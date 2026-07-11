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
       [--profile NAME] [--exclude ZONE [ZONE ...]]
       [--format TEMPLATE] [--date-format STRFTIME] [--time-format STRFTIME]
       [--separator SEP] [--config PATH]
```

- `--from` — source time zone. Accepts an IANA name (`America/Toronto`) or a
  friendly city alias (`Toronto`). See `src/meetingtime/aliases.py` for the full list.
- `--date` — source date as `YYYYMMDD`, e.g. `20260710`.
- `--time` — source time as 24-hour `HHMM`, e.g. `0900`.
- `--to` — one or more target zones/cities. If `--profile` is given, these are
  added on top of the profile's zones. If omitted with no profile, falls back to
  the `timezones` list in your config file, or just the source zone.
- `--profile` — use a named `[profiles.NAME]` section from the config file as
  the base zone list.
- `--exclude` — zones/cities to remove from the final output. Takes precedence
  over all other zone sources including `--to` and `--profile`.
- `--format` — a format name defined in `[format]`, a literal template string
  using `{city} {date} {time} {abbr} {tz}` placeholders, or the special value
  `markdown` for a table. Default: `'{city} ({date}, {time} {abbr})'`.
- `--date-format` — strftime pattern for the `{date}` field. Default: `%b %-d`
  (e.g. `Jul 10`). Example: `--date-format '%Y-%m-%d'` → `2026-07-10`.
  Can also be set via `date_format` in the config file.
- `--time-format` — strftime pattern for the `{time}` field. Default: `%H:%M`
  (e.g. `14:00`). Example: `--time-format '%I:%M %p'` → `02:00 PM`.
  Can also be set via `time_format` in the config file.
- `--separator` — string used to join entries (default `'; '`).
- `--config` — path to a TOML config file (default `~/.config/meetingtime/config.toml`).

## Config file

Avoid retyping your team's zones every time by creating
`~/.config/meetingtime/config.toml`:

```toml
date_format = '%Y-%m-%d'
time_format = '%I:%M %p'

[format]
short   = '{city} {time} {abbr}'
compact = '{city} ({time})'

[profiles.work]
timezones = ['America/Toronto', 'Europe/London', 'Asia/Tokyo']
format = 'short'

[profiles.asia]
timezones = ['Asia/Singapore', 'Asia/Hong_Kong', 'Asia/Tokyo']
```

See [examples/config.toml](examples/config.toml) for a more complete example.

Then run with a profile:

```
meetingtime --from Toronto --date 20260710 --time 0900 --profile work
```

Add extra zones on top of the profile:

```
meetingtime --from Toronto --date 20260710 --time 0900 --profile work --to Singapore
```

Exclude a zone from the output:

```
meetingtime --from Toronto --date 20260710 --time 0900 --profile work --exclude Tokyo
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
