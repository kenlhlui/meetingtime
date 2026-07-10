# meetingtime

Convert one date + time into a nicely formatted summary across many time zones.

```
meetingtime --from America/Toronto --date 20260710 --time 0900 \
    --to Toronto London 'Los Angeles' Tokyo
```

```
Toronto (Jul 10, 09:00 EDT); London (Jul 10, 14:00 BST); Los Angeles (Jul 10, 06:00 PDT); Tokyo (Jul 10, 22:00 JST)
```

## Install / run

With [uv](https://docs.astral.sh/uv/) (no install needed):

```
uvx --from /path/to/meetingtime meetingtime --from Toronto --date 20260710 --time 0900 --to London Tokyo
```

Or install it as a persistent tool:

```
uv tool install /path/to/meetingtime
meetingtime --from Toronto --date 20260710 --time 0900 --to London Tokyo
```

Or with plain pip:

```
pip install /path/to/meetingtime
```

## Usage

```
meetingtime --from ZONE --date YYYYMMDD --time HHMM [--to ZONE [ZONE ...]]
       [--format TEMPLATE] [--separator SEP] [--config PATH]
```

- `--from` — source time zone. Accepts an IANA name (`America/Toronto`) or a
  friendly city alias (`Toronto`). See `src/meetingtime/aliases.py` for the full list.
- `--date` — source date as `YYYYMMDD`, e.g. `20260710`.
- `--time` — source time as 24-hour `HHMM`, e.g. `0900`.
- `--to` — one or more target zones/cities. If omitted, falls back to the
  `timezones` list in your config file, or just the source zone.
- `--format` — a template string using `{city} {date} {time} {abbr} {tz}`
  placeholders, or the special value `markdown` for a table. Default:
  `'{city} ({date}, {time} {abbr})'`.
- `--separator` — string used to join entries (default `'; '`).
- `--config` — path to a TOML config file (default `~/.config/meetingtime/config.toml`).

## Config file

Avoid retyping your team's zones every time by creating
`~/.config/meetingtime/config.toml`:

```toml
timezones = [
    'America/Toronto',
    'Europe/London',
    'America/Los_Angeles',
    'Asia/Tokyo',
]
format = '{city} ({date}, {time} {abbr})'
```

Then just run:

```
meetingtime --from Toronto --date 20260710 --time 0900
```

## Markdown table output

```
meetingtime --from Toronto --date 20260710 --time 0900 --to Toronto London Tokyo --format markdown
```

```
| City | Time |
| --- | --- |
| Toronto | Jul 10, 09:00 EDT |
| London | Jul 10, 14:00 BST |
| Tokyo | Jul 10, 22:00 JST |
```
