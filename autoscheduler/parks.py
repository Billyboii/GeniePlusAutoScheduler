"""
Module for manipulating parks info

"""
from typing import List, Dict
from requests import sessions

def get_theme_parks(session: sessions.Session) -> List:
    """
        Fetch references to parks on the API
    """
    parks_json = session.get(
        "https://api.wdpro.disney.go.com/global-pool-override-B"
        "/facility-service/theme-parks").json()

    parks = []
    for park in parks_json.get('entries', {}):
        parks.append(park.get('links', {}).get('self', {}).get('href', {}))

    return parks


def get_water_parks(session: sessions.Session) -> List:
    """
        Fetch references to parks on the API
    """
    parks_json = session.get(
        "https://api.wdpro.disney.go.com/global-pool-override-B"
        "/facility-service/water-parks").json()

    parks = []
    for park in parks_json.get('entries', {}):
        parks.append(park.get('links', {}).get('self', {}).get('href', {}))

    return parks


def get_water_park(session: sessions.Session, identifier: int) -> Dict:
    """
        Fetches water park json from disney, given a session and identifier
    """
    water_park = session.get(
        "https://api.wdpro.disney.go.com/global-pool-override-B"
        f"/facility-service/water-parks/{identifier}").json()
    return water_park


def get_theme_park(session: sessions.Session, identifier: int) -> Dict:
    """
        Fetches a them park json from disney given a session and identifier
    """
    theme_park = session.get(
        "https://api.wdpro.disney.go.com/global-pool-override-B"
        f"/facility-service/theme-parks/{identifier}").json()
    return theme_park
