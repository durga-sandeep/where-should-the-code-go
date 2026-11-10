# Post-hoc exact-content and source-split audit

| Screen | Development / heldout | Duplicate excess (dev / heldout) | Shared distinct hashes |
| --- | ---: | ---: | ---: |
| synthetic_public_payload | 24 / 96 | 0 / 0 | 0 |
| synthetic_id_and_display_ignored_content | 24 / 96 | 0 / 0 | 0 |
| profile_public_payload | 16 / 48 | 0 / 0 | 0 |
| profile_id_and_display_ignored_content | 16 / 48 | 0 / 0 | 0 |
| profile_quantized_past_and_future_sequences | 16 / 48 | 0 / 0 | 0 |

Profile source-store overlap: 0.

- Added after final model results; no examples are removed or rescored.
- Final heldout tasks come from manifests; frozen hash-verified generators recreate 24 v2 development histories and all 16 profile development stores. Only four profile development stores received model calls. Early v1 development is outside this check.
- Generator reproduction of both complete heldout manifests is required. Development manifests are not needed by this packaged check.
- Public-payload checks retain event IDs. The additional content screen ignores IDs/display order but retains revision groups; it also ignores ID tie-breaking and is not a semantic-equivalence test.
- Quantity checks compare exact ordered 36 historical and 12 future quantized sales bins, without receipts or reporting anomalies.
- Paired controls and repetitions deliberately reuse bases and are not included as accidental duplicates.
- Exact matches only: no near-duplicate, linguistic similarity, or provider training-data audit. Public retail profiles may have appeared in training; provider training data are unavailable.
- Disjoint stores can share products, dates, cities and market conditions; source separation does not establish population independence.

Reproduce offline: `python3 audit_overlap.py --output-dir /tmp/temporal-overlap`.
