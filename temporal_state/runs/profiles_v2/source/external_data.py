"""Fetch a pinned, attributed FreshRetailNet subset; no benchmark integration.

Requires pyarrow. Only the 8.44 MB eval partition is downloaded, temporarily.
Source values remain unchanged; they are observed normalized sales, NOT demand.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import tempfile
import urllib.request

import pyarrow
import pyarrow.parquet as pq

REVISION = "08c1fab7f9257bc73679d415d65d644165d351d4"
REPO = "Dingdong-Inc/FreshRetailNet-50K"
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/{REVISION}"
SOURCE_SHA256 = "1b118840664280c6b88bffc84c80ee1f54c05d911e354b7599e5da10995e960e"
SEED = "temporal-state-external-v1"
COLUMNS = ["city_id", "store_id", "product_id", "dt", "sale_amount",
           "hours_sale", "hours_stock_status", "stock_hour6_22_cnt"]


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def rank(kind: str, *ids: int) -> str:
    return digest((SEED + ":" + kind + ":" + ":".join(map(str, ids))).encode())


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--source-parquet", type=Path,
                        help="Optional cached eval file; SHA-256 is always checked")
    parser.add_argument("--stores", type=int, default=64)
    args = parser.parse_args()
    if args.stores < 1:
        raise ValueError("--stores must be positive")
    card = fetch(BASE + "/README.md")
    if b"license: cc-by-4.0" not in card:
        raise ValueError("Expected dataset license not found")
    blob = (args.source_parquet.read_bytes() if args.source_parquet
            else fetch(BASE + "/data/eval.parquet"))
    if digest(blob) != SOURCE_SHA256:
        raise ValueError("Pinned eval partition failed SHA-256 verification")
    with tempfile.TemporaryDirectory(prefix="temporal-frn-") as tmp:
        source = Path(tmp) / "eval.parquet"
        source.write_bytes(blob)
        table = pq.read_table(source, columns=COLUMNS)
    # Select by identifiers alone, before observing sales, stockouts, or results.
    stores = sorted(set(table["store_id"].to_pylist()), key=lambda s: rank("store", s))
    if args.stores > len(stores):
        raise ValueError("Requested more stores than source contains")
    selected_stores = set(stores[:args.stores])
    import pyarrow.compute as pc
    filtered = table.filter(pc.is_in(table["store_id"], value_set=pyarrow.array(sorted(selected_stores))))
    groups = defaultdict(list)
    for row in filtered.to_pylist():
        groups[(row["store_id"], row["product_id"])].append(row)
    selected = []
    identities = []
    for store in stores[:args.stores]:
        products = [product for s, product in groups if s == store]
        product = min(products, key=lambda p: rank("product", store, p))
        window = sorted(groups[store, product], key=lambda r: r["dt"])
        dates = [date.fromisoformat(r["dt"]) for r in window]
        assert len(window) == 7 and len(set(dates)) == 7
        assert all((b - a).days == 1 for a, b in zip(dates, dates[1:]))
        for row in window:
            assert len(row["hours_sale"]) == len(row["hours_stock_status"]) == 24
            assert all(x >= 0 for x in row["hours_sale"])
            assert set(row["hours_stock_status"]) <= {0, 1}
        selected.extend(window)
        identities.append({"store_id": store, "product_id": product,
                           "city_id": window[0]["city_id"]})
    selected.sort(key=lambda r: (r["store_id"], r["product_id"], r["dt"]))
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    subset = b"".join((json.dumps(r, sort_keys=True, separators=(",", ":"),
                                allow_nan=False) + "\n").encode() for r in selected)
    (output / "freshretail_profiles.jsonl").write_bytes(subset)
    (output / "freshretail_SOURCE_README.md").write_bytes(card)
    manifest = {
        "dataset": REPO, "revision": REVISION, "source_split": "eval",
        "source_url": BASE + "/data/eval.parquet", "source_sha256": digest(blob),
        "source_bytes": len(blob), "source_rows": table.num_rows,
        "source_card_url": BASE + "/README.md", "source_card_sha256": digest(card),
        "license": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Dingdong-Inc, FreshRetailNet-50K, version 1.0; Wang et al. (2025), arXiv:2505.16319",
        "selection": "SHA-256 rank store IDs, first N; SHA-256 rank product IDs within each selected store, first; all seven eval dates. No outcome or sales screening.",
        "selection_seed": SEED, "source_distinct_stores": len(stores),
        "selected_store_product_ids": identities, "stores": len(identities),
        "rows": len(selected), "hours": 24 * len(selected), "columns": COLUMNS,
        "start_date": min(r["dt"] for r in selected), "end_date": max(r["dt"] for r in selected),
        "subset_sha256": digest(subset), "subset_bytes": len(subset),
        "distinct_products": len({r["product_id"] for r in selected}),
        "distinct_cities": len({r["city_id"] for r in selected}),
        "zero_sale_days": sum(sum(r["hours_sale"]) == 0 for r in selected),
        "zero_sale_windows": sum(all(sum(r["hours_sale"]) == 0 for r in selected if r["store_id"] == s) for s in selected_stores),
        "reported_out_of_stock_hours": sum(sum(r["hours_stock_status"]) for r in selected),
        "modifications": "Subset of rows and columns only. Numeric source values unchanged; no scaling, rounding, demand recovery or simulated events added.",
        "limitations": "Normalized observed sales can be stockout-censored; not latent demand. No event receipt/correction timestamps, receipts, or on-hand inventory. Distinct stores are not a guarantee of independent samples.",
        "pyarrow_version": pyarrow.__version__,
    }
    (output / "freshretail_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: manifest[k] for k in ["stores", "rows", "hours", "subset_sha256", "zero_sale_windows"]}, indent=2))


if __name__ == "__main__":
    main()
