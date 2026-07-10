"""Optional config file support for meetingtime.

Looks for a config file at (in order):
  1. the path given via --config
  2. $XDG_CONFIG_HOME/meetingtime/config.toml
  3. ~/.config/meetingtime/config.toml

Example config file:

    # ~/.config/meetingtime/config.toml
    timezones = [
        'America/Toronto',
        'Europe/London',
        'America/Los_Angeles',
        'Asia/Tokyo',
    ]
    format = '{city} ({date}, {time} {abbr})'

    [profiles.work]
    timezones = ['America/Toronto', 'Europe/London']

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


def config_timezones(config: dict[str, Any]) -> list[str] | list:
    """Extract the 'timezones' list from a loaded config dict, if present."""
    zones = config.get("timezones", [])
    return list(zones) if isinstance(zones, list) else []


def config_profile_timezones(config: dict[str, Any], profile_name: str) -> list[str]:
    """Extract timezones for a named profile, or [] if the profile doesn't exist."""
    profile = config.get("profiles", {}).get(profile_name, {})
    zones = profile.get("timezones", [])
    return list(zones) if isinstance(zones, list) else []


def config_format(config: dict[str, Any]) -> str | None:
    """Extract the 'format' template string from a loaded config dict, if present."""
    value = config.get("format")
    return value if isinstance(value, str) else None
