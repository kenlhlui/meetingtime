"""Friendly city-name aliases that map to IANA time zone names.

This is intentionally a small, opinionated list of commonly used cities.
Anything not in this table can still be used by passing the full IANA
name directly, e.g. '--to Asia/Kolkata'.
"""

# 'key' is lower-cased and stripped of spaces/underscores for lookup.
CITY_ALIASES = {
    # Canada
    "toronto": "America/Toronto",
    "ottawa": "America/Toronto",
    "montreal": "America/Toronto",
    "quebec": "America/Toronto",
    "hamilton": "America/Toronto",
    "kitchener": "America/Toronto",
    "london_on": "America/Toronto",
    "vancouver": "America/Vancouver",
    "victoria": "America/Vancouver",
    "kelowna": "America/Vancouver",
    "calgary": "America/Edmonton",
    "edmonton": "America/Edmonton",
    "winnipeg": "America/Winnipeg",
    "regina": "America/Regina",
    "saskatoon": "America/Regina",  # ponytail: SK has no DST, Regina zone covers both
    "halifax": "America/Halifax",
    "moncton": "America/Halifax",
    "charlottetown": "America/Halifax",
    "fredericton": "America/Halifax",
    "stjohns": "America/St_Johns",
    "newfoundland": "America/St_Johns",
    # United States
    "newyork": "America/New_York",
    "nyc": "America/New_York",
    "boston": "America/New_York",
    "miami": "America/New_York",
    "atlanta": "America/New_York",
    "philadelphia": "America/New_York",
    "washington": "America/New_York",
    "dc": "America/New_York",
    "losangeles": "America/Los_Angeles",
    "la": "America/Los_Angeles",
    "sanfrancisco": "America/Los_Angeles",
    "sf": "America/Los_Angeles",
    "seattle": "America/Los_Angeles",
    "portland": "America/Los_Angeles",
    "lasvegas": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "dallas": "America/Chicago",
    "houston": "America/Chicago",
    "minneapolis": "America/Chicago",
    "denver": "America/Denver",
    "phoenix": "America/Phoenix",
    "mexicocity": "America/Mexico_City",
    "saopaulo": "America/Sao_Paulo",
    "buenosaires": "America/Argentina/Buenos_Aires",
    # Europe
    "london": "Europe/London",
    "uk": "Europe/London",
    "dublin": "Europe/Dublin",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "madrid": "Europe/Madrid",
    "barcelona": "Europe/Madrid",
    "rome": "Europe/Rome",
    "milan": "Europe/Rome",
    "amsterdam": "Europe/Amsterdam",
    "brussels": "Europe/Brussels",
    "zurich": "Europe/Zurich",
    "geneva": "Europe/Zurich",
    "vienna": "Europe/Vienna",
    "warsaw": "Europe/Warsaw",
    "stockholm": "Europe/Stockholm",
    "oslo": "Europe/Oslo",
    "copenhagen": "Europe/Copenhagen",
    "helsinki": "Europe/Helsinki",
    "athens": "Europe/Athens",
    "moscow": "Europe/Moscow",
    "istanbul": "Europe/Istanbul",
    # Middle East & Africa
    "dubai": "Asia/Dubai",
    "abudhabi": "Asia/Dubai",
    "riyadh": "Asia/Riyadh",
    "cairo": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg",
    "lagos": "Africa/Lagos",
    "nairobi": "Africa/Nairobi",
    "accra": "Africa/Accra",
    "casablanca": "Africa/Casablanca",
    # Asia
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "india": "Asia/Kolkata",
    "kolkata": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata",
    "hyderabad": "Asia/Kolkata",
    "chennai": "Asia/Kolkata",
    "karachi": "Asia/Karachi",
    "dhaka": "Asia/Dhaka",
    "bangkok": "Asia/Bangkok",
    "jakarta": "Asia/Jakarta",
    "singapore": "Asia/Singapore",
    "kualalumpur": "Asia/Kuala_Lumpur",
    "kl": "Asia/Kuala_Lumpur",
    "hongkong": "Asia/Hong_Kong",
    "hk": "Asia/Hong_Kong",
    "shanghai": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "taipei": "Asia/Taipei",
    "seoul": "Asia/Seoul",
    "tokyo": "Asia/Tokyo",
    "osaka": "Asia/Tokyo",
    "manila": "Asia/Manila",
    # Pacific & Oceania
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "brisbane": "Australia/Brisbane",
    "perth": "Australia/Perth",
    "auckland": "Pacific/Auckland",
    "honolulu": "Pacific/Honolulu",
    # UTC
    "utc": "UTC",
    "gmt": "UTC",
}

# Display name overrides for aliases where the IANA city part is misleading.
# Only entries that differ from the IANA-derived name are listed here.
ALIAS_DISPLAY = {
    "ottawa": "Ottawa",
    "montreal": "Montreal",
    "quebec": "Quebec City",
    "hamilton": "Hamilton",
    "kitchener": "Kitchener",
    "london_on": "London (ON)",
    "victoria": "Victoria",
    "kelowna": "Kelowna",
    "moncton": "Moncton",
    "charlottetown": "Charlottetown",
    "fredericton": "Fredericton",
    "stjohns": "St. John's",
    "newfoundland": "Newfoundland",
    "boston": "Boston",
    "miami": "Miami",
    "atlanta": "Atlanta",
    "philadelphia": "Philadelphia",
    "washington": "Washington DC",
    "dc": "Washington DC",
    "nyc": "New York",
    "seattle": "Seattle",
    "portland": "Portland",
    "lasvegas": "Las Vegas",
    "dallas": "Dallas",
    "houston": "Houston",
    "minneapolis": "Minneapolis",
    "phoenix": "Phoenix",
    "sf": "San Francisco",
    "sanfrancisco": "San Francisco",
    "la": "Los Angeles",
    "uk": "London",
    "barcelona": "Barcelona",
    "milan": "Milan",
    "brussels": "Brussels",
    "geneva": "Geneva",
    "abudhabi": "Abu Dhabi",
    "riyadh": "Riyadh",
    "accra": "Accra",
    "casablanca": "Casablanca",
    "mumbai": "Mumbai",
    "delhi": "Delhi",
    "india": "India",
    "bangalore": "Bangalore",
    "hyderabad": "Hyderabad",
    "chennai": "Chennai",
    "beijing": "Beijing",
    "osaka": "Osaka",
    "kualalumpur": "Kuala Lumpur",
    "kl": "Kuala Lumpur",
    "hk": "Hong Kong",
    "brisbane": "Brisbane",
    "gmt": "UTC",
}


def normalize_key(name: str) -> str:
    """Lower-case a name and strip spaces/underscores so lookups are forgiving."""
    return name.strip().lower().replace(" ", "").replace("_", "")


def resolve_timezone(name: str) -> str:
    """Resolve a user-supplied city/zone string to an IANA time zone name.

    Accepts either a friendly alias (e.g. 'Toronto') or a full IANA name
    (e.g. 'America/Toronto'). Returns the IANA name unchanged if it already
    looks like one (contains a '/') or is 'UTC'.
    """
    if name.upper() == "UTC" or "/" in name:
        return name
    key = normalize_key(name)
    if key in CITY_ALIASES:
        return CITY_ALIASES[key]
    # Fall back to returning the original string; zoneinfo will raise a
    # clear error later if it truly isn't a valid IANA zone.
    return name


def display_name(iana_name: str, raw_hint: str | None = None) -> str:
    """Turn an IANA zone name into a display name.

    If raw_hint is given and matches an ALIAS_DISPLAY entry, that takes priority
    (so 'beijing' shows 'Beijing' rather than 'Shanghai').
    """
    if raw_hint is not None:
        override = ALIAS_DISPLAY.get(normalize_key(raw_hint))
        if override:
            return override
    if iana_name.upper() == "UTC":
        return "UTC"
    city_part = iana_name.rsplit("/", maxsplit=1)[-1]
    return city_part.replace("_", " ")
