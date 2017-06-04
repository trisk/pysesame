"""
Python API to control Sesame smart locks.
"""
from .candyhouse import CandyHouseAccount
from .sesame import Sesame

def get_sesames(email, password, device_ids=[], nicknames=[], timeout=5):
    """Return list of available Sesame objects."""
    sesames = []
    account = CandyHouseAccount(email, password, timeout=timeout)

    for sesame in account.sesames:
        if device_ids and sesame['device_id'] not in device_ids:
            continue
        if nicknames and sesame['nickname'] not in nicknames:
            continue
        sesames.append(Sesame(account, sesame))

    return sesames
