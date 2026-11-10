# FreshRetailNet external-profile subset

Prepared 2026-09-07. This is a reproducible data extraction, with no benchmark integration or model calls.

## Verified origin and permission

The [official Dingdong-Inc dataset](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K) explicitly licenses its data under **CC BY 4.0** and links the [Dingdong-Inc baseline repository](https://github.com/Dingdong-Inc/frn-50k-baseline). The pinned source card is preserved verbatim in `data/freshretail_SOURCE_README.md`, including developer attribution, license link and paper citation. Attribute Dingdong-Inc and Wang et al., *FreshRetailNet-50K: A Stockout-Annotated Censored Demand Dataset for Latent Demand Recovery and Forecasting in Fresh Retail* (2025), [arXiv:2505.16319](https://arxiv.org/abs/2505.16319). Preserve attribution and identify transformations when redistributing derived profiles; license: https://creativecommons.org/licenses/by/4.0/.

Dataset revision: `08c1fab7f9257bc73679d415d65d644165d351d4`.

Only the small `data/eval.parquet` partition was fetched: 8,440,124 bytes, 350,000 daily rows. The 106 MB training partition was not fetched. The source partition SHA-256 is `1b118840664280c6b88bffc84c80ee1f54c05d911e354b7599e5da10995e960e`, verified against the official repository's LFS metadata. The script validates it on every run. The full partition is temporary and is not included in this research package.

## Files and reproducibility

- `external_data.py`: Python standard library plus PyArrow; no pandas or dataset SDK required. Tested with PyArrow 23.0.0.
- `data/freshretail_profiles.jsonl`: 128,864 bytes; 448 daily records covering 64 store-product windows, seven days per window and 10,752 hourly values.
- `data/freshretail_manifest.json`: exact source URL, revision, source/card/output SHA-256 hashes, selected identifiers, selection rule, columns and limitations.
- `data/freshretail_SOURCE_README.md`: unmodified source attribution, schema descriptions, license and citation.

From the workspace root:

```sh
python3 research_sprint/temporal_state/external_data.py
```

The script downloads the pinned 8.44 MB partition and verifies its hash before reading it. An optional `--source-parquet /path/to/eval.parquet` uses an existing copy but still verifies the hash. Use `--output /tmp/frn-check` for independent reproduction. `--stores` changes subset size; the packaged version uses the default 64.

The cached-source run and a separate direct-download run produced **byte-identical JSONL, manifest and source card**. JSONL SHA-256: `3131d97d614b0efcef07f8b1b840d3a9238c30ab1deacbe399328d1f3a8b23f7`. Manifest includes the PyArrow version, so a different runtime version can change manifest bytes without changing extracted data.

## Selection and schema

Selection uses identifiers only, without screening sales, stockouts or model outcomes. SHA-256 rank all 898 store IDs with fixed seed `temporal-state-external-v1`, select the first 64, then SHA-256 rank product IDs within each chosen store and select the first product. Retain all seven evaluation dates (2024-06-26 through 2024-07-02). Final JSONL order is store ID, product ID, date. This gives 64 distinct stores, 58 distinct products and 14 cities. Distinct stores offer source clusters; they do not prove independence because stores can share products, calendar dates and city conditions. Any development/test split should preserve store disjointness, and derived cases from the same window should remain clustered.

Retained fields, with source values unchanged:

| Field | Meaning |
| --- | --- |
| `city_id`, `store_id`, `product_id` | Encoded source identifiers |
| `dt` | Source date string |
| `sale_amount` | Globally normalized observed daily sales |
| `hours_sale` | 24 globally normalized observed hourly sales values |
| `hours_stock_status` | 24 hourly out-of-stock indicators; 1 denotes out of stock |
| `stock_hour6_22_cnt` | Source count of out-of-stock hours between 06:00 and 22:00 |

Assertions check contiguous seven-day windows, 24 values per hourly vector, nonnegative sales, and binary stock-status values. In this unfiltered subset, 36 daily profiles have zero total sales, including one entirely zero-sales seven-day window. There are 2,768 source out-of-stock hourly flags, counting all 24 hours per day. These observations are descriptive, not grounds for silently excluding profiles. If a later simulator requires a positive-demand profile, document any exclusion or alternate selection before evaluating models.

## Permitted interpretation in the proposed experiment

These are **observed normalized sales profiles**, not recovered true demand. Source stockouts censor sales; normalization means values are not literal item counts. No rescaling, rounding or demand imputation is performed here. A later simulator can explicitly map these values to synthetic scenario-demand inputs, documenting its transformation and retaining source profile identifiers.

The dataset does not supply the proposed event receipt times, late reports, correction chains, inventory receipts or exact on-hand trajectories. These must remain **synthetically generated**. A defensible description is “a controlled inventory simulation driven by temporal profiles from public retail sales.” It is not real-world validation of late-report frequency, bitemporal reconstruction accuracy or uncensored customer demand. An all-zero retained window is a legitimate invariance/control opportunity rather than evidence of failed data extraction.
