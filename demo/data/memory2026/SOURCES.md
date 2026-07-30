# Memory-sector 2026 — vendored data

Daily closes, vendored 2026-07-29 (the last session in every file), so the
demo runs offline with zero API keys — same policy as `demo/data/2008/`.

| File | Instrument | Ticker | Span |
|---|---|---|---|
| skhynix.csv | SK Hynix | 000660.KS | 2021-07-29 → 2026-07-29 |
| samsung.csv | Samsung Electronics | 005930.KS | 2021-07-29 → 2026-07-29 |
| micron.csv | Micron | MU | 2021-07-30 → 2026-07-29 |
| wdc.csv | Western Digital | WDC | 2021-07-30 → 2026-07-29 |
| seagate.csv | Seagate | STX | 2021-07-30 → 2026-07-29 |
| sandisk.csv | SanDisk (post-spinoff) | SNDK | 2025-02-13 → 2026-07-29 |
| soxx.csv | iShares Semiconductor ETF | SOXX | 2021-07-30 → 2026-07-29 |

Source: Yahoo Finance daily chart endpoint (public, keyless). Columns:
`date,close`. Prices in local listing currency; the demo uses log returns
and per-name normalizations only, so currency never enters the statistic.
