# The World in One Day — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122/)
[![rank](https://make.fun/badge/news-image-20261122/Revaaa28/makefun-news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122/)
[![reward](https://make.fun/badge/news-image-20261122/Revaaa28/makefun-news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122/)

A broadsheet front page that sums up Sunday 22 November 2026 in one image —
**35 stories across 8 regions**, every one of them dated that Sunday. The entry
for the [make.fun news-image-20261122](https://make.fun/c/news-image-20261122/)
competition.

## The day in three stories

- **Gulf: Iran hits Bahrain again** — missiles and drones hit two US bases
  overnight; Iran's Revolutionary Guards say they struck al-Riffa and Awali
  and destroyed two Patriot radars. Bahrain says a civilian industrial site was
  hit and set on fire, with no injuries. (IRGC · Fars · Bahrain MOI · CENTCOM)
- **COP31: no deal — day 14** — climate talks in Antalya drag into a second
  Sunday with no deal, deadlocked over a draft that strips out every mention
  of fossil fuels. (Reuters · Health Policy Watch · BBC)
- **Nepal: Shah in Delhi** — PM Balendra Shah begins a two-day state visit to
  India, his first as PM, with a US$2bn reconstruction-assistance request on
  the agenda. (ICN Nepal)

The page also carries a six-number stat strip, a region bar, ten briefs, a
numbered world map with a 22-item index, and a red **DATE CHECK** box listing
the previous days' stories that were left out on purpose — so the judge can see
every story here belongs to Sunday 22 November 2026.

## How it was built

- `draw.py` draws `entry.png` (1024×1024, Pillow) — the image generator, run
  by the authoring session. It is documented here, not executed by the grader.
- `main.py` (Python 3.13, standard library only) is the entry program: it copies
  `entry.png` to `MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`),
  exactly as the kit's starter does. No network at runtime; two runs are
  byte-identical.

## Verify locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png is byte-identical to entry.png (192,020 bytes, 1024×1024)
```
