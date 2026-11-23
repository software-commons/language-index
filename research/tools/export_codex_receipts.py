"""Extract SCES acquisition receipts from a selected, completed Codex turn."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit


MARKER = "SCES_ACQUISITION_V1 "
IDENTIFIER = r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}"
CALL_ID = r"call_[A-Za-z0-9_-]{1,120}"
LABEL = r"[A-Za-z0-9][A-Za-z0-9._/+:-]{0,127}"
TRACE_PATH = r"sces/artifacts/[a-z0-9][a-z0-9._-]*(?:/[a-z0-9][a-z0-9._-]*)*\.jsonl"
RUNNING_CELL = re.compile(r"Script running with cell ID ([A-Za-z0-9:_-]+)")


class ReceiptError(ValueError):
    """The selected rollout could not be safely exported."""


def require(condition, message):
    if not condition:
        raise ReceiptError(message)


def serialize(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def distinct_fields(pairs):
    value = {}
    for key, field in pairs:
        require(key not in value, "duplicate JSON field in an acquisition marker")
        value[key] = field
    return value


def matches(pattern, value):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def event_time(row):
    timestamp = row.get("timestamp")
    require(isinstance(timestamp, str) and timestamp.endswith("Z"), "event has no UTC timestamp")
    try:
        return datetime.fromisoformat(timestamp[:-1] + "+00:00")
    except ValueError as error:
        raise ReceiptError("invalid UTC timestamp") from error


def sces_time(value):
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def source_marker(line):
    try:
        marker = json.loads(line[len(MARKER):], object_pairs_hook=distinct_fields)
    except json.JSONDecodeError as error:
        raise ReceiptError("invalid JSON in an acquisition marker") from error
    required = {"source", "locator"}
    require(isinstance(marker, dict) and required <= marker.keys() <= required | {"sha256"},
            "unexpected fields in an acquisition marker")
    source = marker["source"]
    require(isinstance(source, dict) and source.keys() == {"kind", "id", "revision"} and
            source["kind"] == "source" and matches(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", source["id"]) and
            type(source["revision"]) is int and source["revision"] > 0,
            "invalid source reference in an acquisition marker")
    uri = marker["locator"]
    require(matches(r"[!-~]{1,2048}", uri), "invalid public locator in an acquisition marker")
    parts = urlsplit(uri)
    require(uri.startswith(("https://", "urn:")) and not parts.query and
            not parts.username and not parts.password and
            (parts.hostname if parts.scheme == "https" else bool(parts.path and not parts.netloc)),
            "acquisition locator must be a public HTTPS URL or URN without credentials or query")
    if "sha256" in marker:
        require(matches(r"[0-9a-f]{64}", marker["sha256"]), "invalid acquisition digest")
    return marker


def markers_in(output):
    if isinstance(output, str):
        blocks = [output]
    elif isinstance(output, list):
        blocks = [block["text"] for block in output if isinstance(block, dict) and
                  block.get("type") in {"input_text", "output_text"} and isinstance(block.get("text"), str)]
    else:
        return
    for block in blocks:
        # functions.exec can emit plain text or a structured tools.exec_command result.
        try:
            result = json.loads(block)
        except json.JSONDecodeError:
            result = None
        if isinstance(result, dict) and "value" in result and result.get("status") == "fulfilled":
            result = result["value"]
        if isinstance(result, dict) and {"chunk_id", "exit_code", "output"} <= result.keys():
            if type(result["exit_code"]) is not int or result["exit_code"] != 0:
                require(MARKER not in str(result["output"]), "acquisition command did not complete successfully")
                continue
            require(isinstance(result["output"], str), "invalid acquisition command output")
            block = result["output"]
        for line in block.splitlines():
            if line.startswith(MARKER):
                yield source_marker(line)


def output_heading(output):
    if isinstance(output, list):
        output = output[0].get("text", "") if output and isinstance(output[0], dict) else ""
    return output.split("\n", 1)[0].rstrip("\r") if isinstance(output, str) else ""


def selected_rollout(path, turn_id):
    match = re.fullmatch(rf"rollout-.*({IDENTIFIER})\.jsonl", path.name)
    require(match is not None, "select an explicit Codex rollout JSONL file")
    thread_id = match[1]
    require(matches(IDENTIFIER, turn_id), "select the exact Codex turn UUID")
    rows = []
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ReceiptError(f"invalid rollout JSON at line {number}") from error
            require(isinstance(row, dict) and isinstance(row.get("payload"), dict),
                    f"invalid rollout shape at line {number}")
            rows.append(row)
    meta = [row["payload"] for row in rows if row.get("type") == "session_meta" and
            row["payload"].get("id") == thread_id]
    require(len(meta) == 1 and matches(LABEL, meta[0].get("cli_version")), "missing or ambiguous harness metadata")
    boundaries = defaultdict(list)
    for index, row in enumerate(rows):
        event = row["payload"]
        if row.get("type") == "event_msg" and event.get("turn_id") == turn_id:
            boundaries[event.get("type")].append(index)
    starts, completions = boundaries["task_started"], boundaries["task_complete"]
    require(len(starts) == len(completions) == 1 and starts[0] < completions[0] and
            not boundaries["turn_aborted"], "turn must have a unique successful start and completion")
    start_index, end_index = starts[0], completions[0]
    start, end = event_time(rows[start_index]), event_time(rows[end_index])
    require(start <= end, "turn completion precedes its start")
    context = [row["payload"] for row in rows[start_index:end_index]
               if row.get("type") == "turn_context" and row["payload"].get("turn_id") == turn_id]
    require(context and all(matches(LABEL, entry.get("model")) for entry in context) and
            len({entry["model"] for entry in context}) == 1, "missing or ambiguous turn model")
    return rows, thread_id, start_index, end_index, start, end, context[0]["model"], meta[0]["cli_version"]


def export(path, turn_id, trace_path, selected_calls):
    require(matches(TRACE_PATH, trace_path) and ".." not in PurePosixPath(trace_path).parts,
            "trace path must be a safe .jsonl path under sces/artifacts")
    rows, thread, begin, end, started, completed, model, version = selected_rollout(path, turn_id)
    require(len(set(selected_calls)) == len(selected_calls) and all(matches(CALL_ID, call) for call in selected_calls),
            "selected call IDs must be valid and unique")
    execution = f"codex-rollout:{thread}:{turn_id}"
    pairs = defaultdict(list)
    for index, row in enumerate(rows):
        payload = row["payload"]
        if row.get("type") == "response_item" and payload.get("type") in {
            "custom_tool_call", "custom_tool_call_output", "function_call", "function_call_output"
        } and matches(CALL_ID, payload.get("call_id")):
            pairs[payload["call_id"]].append(index)

    active_cells = {}

    def request_for(index):
        call = rows[index]["payload"]["call_id"]
        require(matches(CALL_ID, call) and len(pairs[call]) == 2, "marked output lacks a unique input/output pair")
        request_index, response_index = pairs[call]
        require(begin < request_index < response_index == index, "tool call is not paired within the selected turn")
        return request_index, rows[request_index]["payload"]

    trace = []
    used = set()
    for index in range(begin + 1, end):
        row = rows[index]
        payload = row["payload"]
        if row.get("type") != "response_item" or payload.get("type") not in {
            "custom_tool_call_output", "function_call_output"
        }:
            continue
        call, output = payload.get("call_id"), payload.get("output")
        heading = output_heading(output)
        running = RUNNING_CELL.fullmatch(heading)
        if running and payload["type"] == "custom_tool_call_output":
            _, request = request_for(index)
            require(request.get("type") == "custom_tool_call" and request.get("name") == "exec" and
                    request.get("status") == "completed", "yielded output lacks its original functions.exec call")
            cell = running[1]
            require(cell not in active_cells, "ambiguous yielded functions.exec cell")
            active_cells[cell] = index
            continue
        if selected_calls and call not in selected_calls:
            continue
        markers = list(markers_in(output))
        if not markers:
            continue
        request_index, request = request_for(index)
        if payload["type"] == "function_call_output":
            require(request.get("type") == "function_call" and request.get("name") == "wait" and
                    heading == "Script completed", "marked continuation lacks a successful functions.wait result")
            wait = json.loads(request["arguments"])
            require(isinstance(wait, dict), "marked continuation has invalid wait arguments")
            cell = wait.get("cell_id")
            require(not wait.get("terminate") and cell in active_cells and active_cells[cell] < request_index,
                    "marked continuation lacks an earlier functions.exec cell in the same turn")
            del active_cells[cell]
        else:
            require(request.get("type") == "custom_tool_call" and request.get("name") == "exec" and
                    request.get("status") == "completed", "marked output lacks a completed functions.exec call")
        result_time = event_time(row)
        require(started <= event_time(rows[request_index]) <= result_time <= completed,
                "acquisition timestamp is outside its turn")
        used.add(call)
        for ordinal, marker in enumerate(markers, 1):
            trace.append({
                **marker, "execution": execution, "event": "direct-inspection",
                "capture": f"codex-rollout:{thread}:{call}:{ordinal}",
                "retrieved_at": sces_time(result_time),
            })
    require(trace and (not selected_calls or used == set(selected_calls)), "selected turn has missing marked acquisitions")
    trace_bytes = b"".join(map(serialize, trace))
    run = {
        "agent": "codex", "execution": execution, "harness": f"codex/{version}", "model": model,
        "started": sces_time(started), "completed": sces_time(completed),
        "trace": {"path": trace_path, "sha256": sha256(trace_bytes).hexdigest()},
    }
    return trace_bytes, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollout", type=Path, required=True)
    parser.add_argument("--turn", required=True)
    parser.add_argument("--trace-path", required=True, help="repository-relative SCES artifact path")
    parser.add_argument("--call-id", action="append", default=[], help="limit extraction to a named tool-call ID")
    parser.add_argument("--emit", required=True, choices=("trace", "run"))
    args = parser.parse_args()
    try:
        trace, run = export(args.rollout, args.turn, args.trace_path, args.call_id)
        sys.stdout.buffer.write(trace if args.emit == "trace" else serialize(run))
    except (OSError, ValueError) as error:
        message = str(error) if isinstance(error, ReceiptError) else "could not read the selected rollout or marker"
        print(f"SCES receipt export: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
