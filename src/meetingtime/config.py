"""Optional config file support for meetingtime.

Looks for a config file at (in order):
  1. the path given via --config
  2. $XDG_CONFIG_HOME/meetingtime/config.toml
  3. ~/.config/meetingtime/config.toml

Example config file:

    # ~/.config/meetingtime/config.toml
    timezones = ['America/Toronto', 'Europe/London', 'America/Los_Angeles', 'Asia/Tokyo']
    date_format = '%Y-%m-%d'
    time_format = '%I:%M %p'

    [format]
    short   = '{city} {time} {abbr}'
    compact = '{city} ({time})'

    [profiles.work]
    timezones = ['America/Toronto', 'Europe/London']
    format = 'short'

    [profiles.asia]
    timezones = ['Asia/Singapore', 'Asia/Tokyo', 'Asia/Kolkata']
"""

import os
import sys
from pathlib import Path
from typing import Any

# tomllib is stdlib from Python 3.11+; fall back to the 'tomli' backport
# on older interpreters if it happens to be installed, otherwise config
# files are simply skipped (the CLI still works fully via flags).
try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - only hit on Python < 3.11
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]


def default_config_path() -> Path:
    """Return the default config file location, honoring XDG_CONFIG_HOME."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "meetingtime" / "config.toml"


def load_config(explicit_path: str | None) -> dict[str, Any]:
    """Load and return the config dict, or {} if no config file is found/usable."""
    if tomllib is None:
        if explicit_path:
            print(
                'Warning: no TOML parser available (Python < 3.11 without "tomli" '
                "installed); ignoring --config.",
                file=sys.stderr,
            )
        return {}

    path = Path(explicit_path) if explicit_path else default_config_path()
    if not path.is_file():
        if explicit_path:
            print(f"Warning: config file not found: {path}", file=sys.stderr)
        return {}

    with path.open("rb") as fh:
        return tomllib.load(fh)


def config_date_format(config: dict[str, Any]) -> str | None:
    value = config.get("date_format")
    return value if isinstance(value, str) else None


def config_time_format(config: dict[str, Any]) -> str | None:
    value = config.get("time_format")
    return value if isinstance(value, str) else None


def config_timezones(config: dict[str, Any]) -> list[str] | list:
    """Extract the 'timezones' list from a loaded config dict, if present."""
    zones = config.get("timezones", [])
    return list(zones) if isinstance(zones, list) else []


def _profile(config: dict[str, Any], profile_name: str) -> dict[str, Any]:
    return config.get("profiles", {}).get(profile_name, {})


def config_profile_timezones(config: dict[str, Any], profile_name: str) -> list[str]:
    """Extract timezones for a named profile, or [] if the profile doesn't exist."""
    zones = _profile(config, profile_name).get("timezones", [])
    return list(zones) if isinstance(zones, list) else []


def config_profile_format(config: dict[str, Any], profile_name: str) -> str | None:
    """Resolve the format for a named profile via [format] lookup, or None."""
    value = _profile(config, profile_name).get("format")
    return resolve_format(config, value) if isinstance(value, str) else None


def config_named_formats(config: dict[str, Any]) -> dict[str, str]:
    """Return the [format] table of named format strings, or {}."""
    section = config.get("format", {})
    return (
        {k: v for k, v in section.items() if isinstance(v, str)}
        if isinstance(section, dict)
        else {}
    )


def resolve_format(config: dict[str, Any], name_or_template: str | None) -> str | None:
    """Resolve a format name or literal template to a template string.

    If name_or_template matches a key in [format], return that template.
    Otherwise return it as-is (literal template or None).
    """
    if name_or_template is None:
        return None
    named = config_named_formats(config)
    return named.get(name_or_template, name_or_template)
