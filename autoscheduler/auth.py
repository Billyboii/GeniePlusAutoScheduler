"""
    Auth contains code for obtaining a client token
"""
from typing import Dict
from requests import sessions

def set_auth_token(session: sessions.Session) -> sessions.Session :
    """
        Sets the auth token on the given session
    """
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/108.0.0.0 Safari/537.36',
        'Accept-Language' : 'en_US',
        'Cache-Control' : '0',
        'Accept' : 'application/json;apiversion=1',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Connection' : 'keep-alive',
        'Proxy-Connection' : 'keep-alive',
        'Accept-Encoding' : 'gzip, deflate'
    }

    auth = session.get(
        "https://disneyworld.disney.go.com/authentication/get-client-token", timeout=10).json()

    session.headers = {
        "Authorization": f"BEARER {auth['access_token']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/108.0.0.0 Safari/537.36',
        "Content-Type": "application/json;charset=UTF-8",
        "Accept":"*/*",
    }
    return session


def get_session() -> sessions.Session:
    """
        Creates a session for calling Disney
    """
    return set_auth_token(sessions.Session())
