""" access_token.py
Creator: Ethan Liu
Date Created: 2024-06-05
Last Modified: 2024-06-05

This file automatically refreshes a short-lived token to a long-lived token
for the Facebook/Instagram Graph API if needed. It also computes the expiry date
automatically for every refresh made (approximately 50 days, 10 days before
token actually expires).

Note that this bot uses a PAGE access token. It has no expiration date. I'm
storing the tokens in a text file because I don't know a better way to do it.
To refresh user token, see the following steps.

Step 1:
Get a short-lived access token from facebook developer and copy-paste it into
the "access_token_short.txt" file.

Step 2:
Run this script.

This script automatically converts the short-lived token into a long-lived user
and page token. It will then be overwritten in the appropriate files for other
scripts to access. Furthermore, the next expiry date will be overwritten in the
"access_token_expire_data.txt" file for other scripts to access as well.

Perchance, "access_token_long.txt" and "access_token_page.txt" are not posted
on the GitHub repository as it's a good practice, perchance. Not sure how to
hide sensitive information yet, but I will learn and get better, perchance.
"""
import requests
import config
from datetime import datetime, timedelta
from exceptions import UserLongTokenError, PageLongTokenError


def get_short_access_token() -> str:
    """ Retrieves the short access token from "access_token_short.txt" file
    and returns it. The token is stored as a string on a single line.
    """
    f = open(config.short_token_file, 'r')
    s = f.read()
    f.close()
    return s


def get_long_access_token() -> str:
    """ Retrieves the long access token from "access_token_long.txt" file
    and returns it. The token is stored as a string on a single line.
    """
    f = open(config.long_token_file, 'r')
    s = f.read()
    f.close()
    return s


def update_access_token_file(token: str, filename: str) -> None:
    """ Overwrites <filename> file with the new long-lived access
    token (PAGE) generated. Stored as a string in on a single line.
    """
    f = open(filename, 'w')
    f.write(token)
    f.close()


def get_expire_date() -> datetime:
    """ Retrieves the expiry date of the current token and returns it.
    The format is YYYY-MM-DD and the time is set at 00:00:00.
    """
    f = open(config.expire_date_file, 'r')
    d = datetime.strptime(f.readline(), '%Y-%m-%d')
    f.close()
    return d


def token_expired() -> bool:
    """ Determines whether the token is going to expire soon (in 10 days)
    """
    expire_date = get_expire_date()
    return expire_date <= datetime.today()


def update_expire_date() -> None:
    """ Calculates the expiry date of the newly refreshed token. The date is
    set at 50 days from the refresh, 10 days before it actually expires.
    Updates the time in "access_token_expire_date.txt" file.
    """
    d = timedelta(days=50)
    today = datetime.today()
    expire_date = today + d
    f = open(config.expire_date_file, 'w')
    f.write(expire_date.strftime('%Y-%m-%d'))


def get_long_user_token(access_token_short: str) -> dict:
    """ Step 1/2 of getting a page access token for Facebook Graph API.

    Converts <access_token_short> into a long-lived **USER** token by sending
    an url request. Returns the request response as a dictionary.

    The returned dictionary contains:
    {
        'access_token': {long-lived-user-access-token},
        'token_type': "bearer",
        'expires_in': {seconds until the short token expires}
    }

    Raises UserLongTokenError when request response status code is not 200.
    Error message does not contain details of error extra debugging is
    necessary.
    """
    url = (f'{config.facebook_graph_url_head}/{config.api_ver}/'
           f'oauth/access_token')
    payload = {
        'grant_type': 'fb_exchange_token',
        'client_id': {config.app_id},
        'client_secret': {config.app_secret},
        'fb_exchange_token': {access_token_short}
    }

    r = requests.get(url, params=payload)

    if r.status_code == 200:
        return r.json()

    raise UserLongTokenError


def get_long_page_access_toke(token: str) -> dict:
    """ Step 2/2 of getting a page access token for Facebook Graph API.

    Converts <token> into a long-lived **PAGE** token by sending an url
    request. Returns the request response as a dictionary.

    The returned dictionary contains:
    {
        'access_token': {page-access-token},
        'id': {page-id}
    }

    Raises PageLongTokenError when request response status code is not 200.
    Error message does not contain details of error extra debugging is
    necessary.
    """
    url = f'{config.facebook_graph_url_head}/{config.fb_page_id}'
    payload = {
        'fields': 'access_token',
        'access_token': token
    }

    r = requests.get(url, params=payload)

    if r.status_code == 200:
        return r.json()

    raise PageLongTokenError


if __name__ == '__main__':
    short_access_token = get_short_access_token()
    long_user_token = get_long_user_token(short_access_token)['access_token']
    long_page_token = get_long_page_access_toke(long_user_token)['access_token']

    update_access_token_file(long_user_token, config.long_token_file)
    update_access_token_file(long_page_token, config.page_token_file)
    update_expire_date()
