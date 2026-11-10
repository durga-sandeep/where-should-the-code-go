"""Deterministic fictional pagination tasks; no network or paid model calls.

generate_tasks(40) makes 40 independent collections crossed with four requests
(160 task dictionaries). Repeated requests/interfaces on a collection are paired,
not independent observations. Only prompt and tool responses go to the agent.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import random
from typing import Any


QUERY_TYPES = ("one", "all", "count", "none")
PAGE_COUNTS = (1, 3, 6)
MATCH_LAYOUTS = ("early", "late", "spread", "zero")
LIST_RECORDS_TOOL = {
    "name": "list_records",
    "description": (
        "Read the collection in pages. Omit cursor or pass null for the first "
        "page. To read the next page, pass exactly the returned next_cursor. "
        "A null next_cursor means the collection is exhausted. Records are "
        "not filtered; inspect their fields against the requested conditions."
    ),
    "parameters": {
        "type": "object",
        "properties": {"cursor": {"type": ["string", "null"]}},
        "additionalProperties": False,
    },
}


def matches(record: dict, query: dict) -> bool:
    """Public predicate semantics, independently evaluated by tests."""
    return (
        record["category"] == query["category"]
        and record["status"] == query["status"]
        and record["score"] >= query["min_score"]
    )


def generate_tasks(n_base: int = 40, seed: int = 20260907) -> list[dict]:
    """Return n_base * 4 JSON-serializable tasks with balanced condition cycling.

    Page/layout combinations cycle through the 12-cell factorial design. At
    n_base=40 each cell has 3 or 4 independent collections. A one-page collection
    cannot distinguish early from late pages; retain the assigned layout label
    but use effective_layout='single_page' for nonzero cases in analysis.
    """
    if isinstance(n_base, bool) or not isinstance(n_base, int) or n_base < 0:
        raise ValueError("n_base must be a nonnegative integer")
    conditions = list(itertools.product(PAGE_COUNTS, MATCH_LAYOUTS))
    random.Random(seed).shuffle(conditions)
    categories = ("alpha", "beta", "gamma", "delta")
    statuses = ("open", "closed", "pending")
    tasks = []
    for index in range(n_base):
        rng = random.Random(f"{seed}:collection:{index}")
        pages, layout = conditions[index % len(conditions)]
        page_size = 5
        size = pages * page_size
        base_id = f"s{seed}-b{index:04d}"
        query = {
            "category": rng.choice(categories),
            "status": rng.choice(statuses),
            "min_score": rng.choice((40, 55, 70)),
        }
        if layout == "zero":
            positive_positions = set()
        elif layout in ("early", "late"):
            start = 0 if layout == "early" else (pages - 1) * page_size
            positive_positions = set(rng.sample(range(start, start + page_size), rng.randint(1, 3)))
        else:
            positive_positions = {
                page * page_size + rng.randrange(page_size) for page in range(pages)
            }
        records = []
        for position in range(size):
            record_id = "R-" + hashlib.sha256(
                f"{base_id}:record:{position}".encode()
            ).hexdigest()[:12]
            record = {
                "id": record_id,
                "category": rng.choice(categories),
                "status": rng.choice(statuses),
                "score": rng.randint(0, 100),
            }
            if position in positive_positions:
                record.update(
                    category=query["category"], status=query["status"],
                    score=rng.randint(query["min_score"], 100),
                )
            elif matches(record, query):
                # Invalidate one random predicate; do not make decoys share a
                # single telltale field or leak positive positions through IDs.
                field = rng.choice(("category", "status", "score"))
                if field == "score":
                    record[field] = rng.randrange(query["min_score"])
                else:
                    options = categories if field == "category" else statuses
                    record[field] = rng.choice([x for x in options if x != query[field]])
            records.append(record)
        target_ids = [record["id"] for record in records if matches(record, query)]
        # Alternate wording on successive repetitions of the factorial grid,
        # rather than confounding wording with the parity of a condition cell.
        template_id = (index // len(conditions)) % 2
        condition_text = (
            f"category equals '{query['category']}', status equals '{query['status']}', "
            f"and score is at least {query['min_score']}"
        )
        if template_id == 0:
            preamble = f"In this fictional collection, a matching record satisfies all conditions: {condition_text}. "
        else:
            preamble = f"Use this fictional record collection. Apply the conjunction of these filters: {condition_text}. "
        requests = {
            "one": 'Return one matching record ID, or no IDs if no record matches. Answer as JSON {"ids": ["ID"]} or {"ids": []}.',
            "all": 'Return every matching record ID, with no duplicates. Answer as JSON {"ids": ["ID", "..."]}; use an empty list if none match.',
            "count": 'Return the exact number of matching records. Answer as JSON {"count": 0}, replacing 0 with the nonnegative integer count.',
            "none": 'Determine whether no matching records exist. Answer as JSON {"none": true} if none exist, or {"none": false} otherwise.',
        }
        for query_type in QUERY_TYPES:
            tasks.append({
                "task_id": f"{base_id}-{query_type}", "base_id": base_id,
                "prompt": preamble + requests[query_type],
                "records": copy.deepcopy(records), "page_size": page_size,
                "target_ids": list(target_ids), "query_type": query_type,
                "query": dict(query), "num_pages": pages,
                "match_layout": layout,
                "effective_layout": "single_page" if pages == 1 and layout != "zero" else layout,
                "template_id": template_id, "seed": seed,
            })
    return tasks


def _cursor(task: dict, offset: int) -> str:
    return "c_" + hashlib.sha256(
        f"{task['base_id']}:page-offset:{offset}".encode()
    ).hexdigest()[:24]


def simulate_tool(task: dict, name: str, args: dict | None, metadata: str = "cursor") -> dict:
    """Read-only pagination. Invalid agent calls return explicit JSON errors.

    The API does not accept query filters. Opaque cursors are collection-specific;
    answers/oracle labels, layout, and total MATCH counts never enter responses.
    'count', 'cursor+total', and 'total' select unfiltered collection metadata.
    """
    if metadata not in ("cursor", "count", "cursor+total", "total"):
        raise ValueError("metadata must be cursor or count (cursor+total/total aliases)")
    if name != "list_records":
        return {"error": "unknown_tool", "message": "Available tool: list_records"}
    if args is None:
        args = {}
    if not isinstance(args, dict) or set(args) - {"cursor"}:
        return {"error": "invalid_arguments", "message": "Only the optional cursor argument is accepted."}
    token = args.get("cursor")
    if token is None:
        offset = 0
    elif not isinstance(token, str):
        return {"error": "invalid_cursor", "message": "Use a returned next_cursor string, or null for the first page."}
    else:
        cursors = {
            _cursor(task, start): start
            for start in range(task["page_size"], len(task["records"]), task["page_size"])
        }
        if token not in cursors:
            return {"error": "invalid_cursor", "message": "Cursor is not valid for this collection."}
        offset = cursors[token]
    stop = offset + task["page_size"]
    response = {
        "records": copy.deepcopy(task["records"][offset:stop]),
        "next_cursor": _cursor(task, stop) if stop < len(task["records"]) else None,
    }
    if metadata != "cursor":
        response.update(
            total_pages=(len(task["records"]) + task["page_size"] - 1) // task["page_size"],
            total_records=len(task["records"]),
        )
    return response


def score_answer(task: dict, answer: Any) -> dict:
    """Exact quantifier-specific scoring; malformed relevant fields fail.

    ID order is irrelevant. Duplicate IDs invalidate one/all answers. Only the
    relevant output key is used; extra keys do not change the score. Precision
    and recall are set measures for 'all'; for 'one', recall means at least one
    correct match was returned. Non-ID task precision/recall are null. false_none
    means an explicit empty/zero/none claim despite actual positive matches.
    """
    result = {
        "exact_success": False, "success": False, "valid_answer": False,
        "precision": None, "recall": None, "count_error": None,
        "false_none": False,
    }
    if not isinstance(answer, dict):
        return result
    truth = set(task["target_ids"])
    query_type = task["query_type"]
    if query_type in ("one", "all"):
        ids = answer.get("ids")
        if not isinstance(ids, list) or any(not isinstance(x, str) for x in ids):
            return result
        predicted = set(ids)
        if len(predicted) != len(ids) or (query_type == "one" and len(ids) > 1):
            return result
        intersection = predicted & truth
        result.update(
            valid_answer=True,
            precision=len(intersection) / len(predicted) if predicted else float(not truth),
            false_none=not predicted and bool(truth),
        )
        if query_type == "all":
            result["recall"] = len(intersection) / len(truth) if truth else float(not predicted)
            result["exact_success"] = predicted == truth
        else:
            result["recall"] = float(bool(intersection)) if truth else float(not predicted)
            result["exact_success"] = bool(intersection) if truth else not predicted
    elif query_type == "count":
        count = answer.get("count")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            return result
        result.update(valid_answer=True, count_error=abs(count - len(truth)),
                      false_none=count == 0 and bool(truth), exact_success=count == len(truth))
    elif query_type == "none":
        none = answer.get("none")
        if not isinstance(none, bool):
            return result
        result.update(valid_answer=True, false_none=none and bool(truth),
                      exact_success=none == (not truth))
    else:
        raise ValueError(f"Unknown query_type: {query_type}")
    result["success"] = result["exact_success"]
    return result


def exhaustive_baseline(task: dict, metadata: str = "cursor") -> dict:
    """Answer by traversing the public tool interface, without target_ids access."""
    found = []
    cursor = None
    while True:
        response = simulate_tool(task, "list_records", {"cursor": cursor}, metadata)
        found.extend(record["id"] for record in response["records"] if matches(record, task["query"]))
        cursor = response["next_cursor"]
        if cursor is None:
            break
    return {
        "one": {"ids": found[:1]}, "all": {"ids": found},
        "count": {"count": len(found)}, "none": {"none": not found},
    }[task["query_type"]]


def task_aware_baseline(task: dict, metadata: str = "cursor", return_trace: bool = False) -> dict:
    """Stop after a witness for one/none; otherwise exhaust accessible pages.

    This is a deterministic engineering baseline, not an LLM result. With
    return_trace=True, return answer plus tool_calls and visited_cursors.
    """
    found, visited = [], []
    cursor = None
    while True:
        visited.append(cursor)
        response = simulate_tool(task, "list_records", {"cursor": cursor}, metadata)
        found.extend(record["id"] for record in response["records"] if matches(record, task["query"]))
        if found and task["query_type"] in ("one", "none"):
            break
        cursor = response["next_cursor"]
        if cursor is None:
            break
    answer = {
        "one": {"ids": found[:1]}, "all": {"ids": found},
        "count": {"count": len(found)}, "none": {"none": not found},
    }[task["query_type"]]
    if return_trace:
        return {"answer": answer, "tool_calls": len(visited), "visited_cursors": visited}
    return answer
