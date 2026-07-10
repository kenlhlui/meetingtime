'''Friendly city-name aliases that map to IANA time zone names.

This is intentionally a small, opinionated list of commonly used cities.
Anything not in this table can still be used by passing the full IANA
name directly, e.g. '--to Asia/Kolkata'.
'''

# 'key' is lower-cased and stripped of spaces/underscores for lookup.
CITY_ALIASES = {
    'toronto': 'America/Toronto',
    'newyork': 'America/New_York',
    'nyc': 'America/New_York',
    'losangeles': 'America/Los_Angeles',
    'la': 'America/Los_Angeles',
    'sanfrancisco': 'America/Los_Angeles',
    'sf': 'America/Los_Angeles',
    'chicago': 'America/Chicago',
    'denver': 'America/Denver',
    'vancouver': 'America/Vancouver',
    'mexicocity': 'America/Mexico_City',
    'saopaulo': 'America/Sao_Paulo',
    'buenosaires': 'America/Argentina/Buenos_Aires',
    'london': 'Europe/London',
    'uk': 'Europe/London',
    'dublin': 'Europe/Dublin',
    'paris': 'Europe/Paris',
    'berlin': 'Europe/Berlin',
    'madrid': 'Europe/Madrid',
    'rome': 'Europe/Rome',
    'amsterdam': 'Europe/Amsterdam',
    'zurich': 'Europe/Zurich',
    'moscow': 'Europe/Moscow',
    'istanbul': 'Europe/Istanbul',
    'dubai': 'Asia/Dubai',
    'mumbai': 'Asia/Kolkata',
    'delhi': 'Asia/Kolkata',
    'india': 'Asia/Kolkata',
    'kolkata': 'Asia/Kolkata',
    'karachi': 'Asia/Karachi',
    'dhaka': 'Asia/Dhaka',
    'bangkok': 'Asia/Bangkok',
    'jakarta': 'Asia/Jakarta',
    'singapore': 'Asia/Singapore',
    'hongkong': 'Asia/Hong_Kong',
    'shanghai': 'Asia/Shanghai',
    'beijing': 'Asia/Shanghai',
    'taipei': 'Asia/Taipei',
    'seoul': 'Asia/Seoul',
    'tokyo': 'Asia/Tokyo',
    'manila': 'Asia/Manila',
    'sydney': 'Australia/Sydney',
    'melbourne': 'Australia/Melbourne',
    'perth': 'Australia/Perth',
    'auckland': 'Pacific/Auckland',
    'honolulu': 'Pacific/Honolulu',
    'cairo': 'Africa/Cairo',
    'johannesburg': 'Africa/Johannesburg',
    'lagos': 'Africa/Lagos',
    'nairobi': 'Africa/Nairobi',
    'utc': 'UTC',
    'gmt': 'UTC',
}


def normalize_key(name: str) -> str:
    '''Lower-case a name and strip spaces/underscores so lookups are forgiving.'''
    return name.strip().lower().replace(' ', '').replace('_', '')


def resolve_timezone(name: str) -> str:
    '''Resolve a user-supplied city/zone string to an IANA time zone name.

    Accepts either a friendly alias (e.g. 'Toronto') or a full IANA name
    (e.g. 'America/Toronto'). Returns the IANA name unchanged if it already
    looks like one (contains a '/') or is 'UTC'.
    '''
    if name.upper() == 'UTC' or '/' in name:
        return name
    key = normalize_key(name)
    if key in CITY_ALIASES:
        return CITY_ALIASES[key]
    # Fall back to returning the original string; zoneinfo will raise a
    # clear error later if it truly isn't a valid IANA zone.
    return name


def display_name(iana_name: str) -> str:
    '''Turn an IANA zone name like America/Los_Angeles into 'Los Angeles'.'''
    if iana_name.upper() == 'UTC':
        return 'UTC'
    city_part = iana_name.split('/')[-1]
    return city_part.replace('_', ' ')
