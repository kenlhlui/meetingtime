"""Command-line entry point for meetingtime.

Convert a single date + time in a source time zone into a nicely
formatted summary across one or more target time zones.

Example:
    meetingtime --from America/Toronto --date 20260710 --time 0900 \\
        --to Toronto London 'Los Angeles' Tokyo
"""

import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from meetingtime import config as cfg
from meetingtime.aliases import display_name, resolve_timezone

DEFAULT_FORMAT = "{city} ({date}, {time} {abbr})"


def parse_args(argv):
    """Build the argparse parser and parse argv into a namespace."""
    parser = argparse.ArgumentParser(
        prog="meetingtime",
        description="Convert a date/time into a formatted summary across many time zones.",
    )
    parser.add_argument(
        "--from",
        dest="from_zone",
        required=True,
        metavar="ZONE",
        help="source time zone, e.g. 'America/Toronto' or 'Toronto'",
    )
    parser.add_argument(
        "--date",
        required=True,
        metavar="YYYYMMDD",
        help="source date, e.g. '20260710'",
    )
    parser.add_argument(
        "--time",
        required=True,
        metavar="HHMM",
        help="source time (24h), e.g. '0900'",
    )
    parser.add_argument(
        "--to",
        nargs="+",
        metavar="ZONE",
        help="one or more target time zones/cities. Defaults to the config "
        "file's 'timezones' list, or just the source zone if none is set.",
    )
    parser.add_argument(
        "--format",
        dest="fmt",
        metavar="TEMPLATE",
        help="output template per zone, using {city} {date} {time} {abbr} {tz} "
        "placeholders. Special value 'markdown' prints a markdown table instead. "
        f"Default: '{DEFAULT_FORMAT}'",
    )
    parser.add_argument(
        "--separator",
        default="; ",
        help="string used to join per-zone entries (default: '; '). Ignored for markdown.",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        help="path to a meetingtime TOML config file (default: ~/.config/meetingtime/config.toml)",
    )
    return parser.parse_args(argv)


def parse_source_datetime(date_str: str, time_str: str, from_zone: str) -> datetime:
    """Parse the --date/--time strings into an aware datetime in from_zone."""
    if len(date_str) != 8 or not date_str.isdigit():
        raise ValueError(f"--date must look like 'YYYYMMDD', got: {date_str!r}")
    if len(time_str) != 4 or not time_str.isdigit():
        raise ValueError(f"--time must look like 'HHMM', got: {time_str!r}")

    year, month, day = int(date_str[0:4]), int(date_str[4:6]), int(date_str[6:8])
    hour, minute = int(time_str[0:2]), int(time_str[2:4])

    try:
        tz = ZoneInfo(resolve_timezone(from_zone))
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown --from time zone: {from_zone!r}") from exc

    return datetime(year, month, day, hour, minute, tzinfo=tz)


def convert_to_zones(source_dt: datetime, zone_names):
    """Convert source_dt into each named zone, returning a list of field dicts."""
    results = []
    for raw_name in zone_names:
        iana_name = resolve_timezone(raw_name)
        try:
            tz = ZoneInfo(iana_name)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown time zone: {raw_name!r}") from exc

        converted = source_dt.astimezone(tz)
        results.append(
            {
                "city": display_name(iana_name),
                "date": converted.strftime("%b %-d")
                if sys.platform != "win32"
                else converted.strftime("%b %#d"),
                "time": converted.strftime("%H:%M"),
                "abbr": converted.strftime("%Z"),
                "tz": iana_name,
            }
        )
    return results


def format_line(entry: dict, template: str) -> str:
    """Fill a single-entry template with that entry's fields."""
    return template.format(**entry)


def format_markdown(entries) -> str:
    """Render entries as a simple markdown table."""
    lines = ["| City | Time |", "| --- | --- |"]
    for entry in entries:
        lines.append(
            f"| {entry['city']} | {entry['date']}, {entry['time']} {entry['abbr']} |"
        )
    return "\n".join(lines)


def main(argv=None) -> int:
    """CLI entry point. Returns a process exit code."""
    args = parse_args(sys.argv[1:] if argv is None else argv)
    config = cfg.load_config(args.config)

    # Resolve which target zones to use: --to flag > config file > just the source zone.
    target_zones = args.to or cfg.config_timezones(config) or [args.from_zone]
    template = args.fmt or cfg.config_format(config) or DEFAULT_FORMAT

    try:
        source_dt = parse_source_datetime(args.date, args.time, args.from_zone)
        entries = convert_to_zones(source_dt, target_zones)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if template == "markdown":
        print(format_markdown(entries))
    else:
        print(args.separator.join(format_line(e, template) for e in entries))

    return 0


if __name__ == "__main__":
    sys.exit(main())
