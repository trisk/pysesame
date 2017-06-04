"""
Python API to control Sesame smart locks.
"""
from .candyhouse import CandyHouseAccount
from .sesame import Sesame


def get_sesames(email, password, device_ids=None, nicknames=None, timeout=5):
    """Return list of available Sesame objects."""
    sesames = []
    account = CandyHouseAccount(email, password, timeout=timeout)

    for sesame in account.sesames:
        if device_ids is not None and sesame['device_id'] not in device_ids:
            continue
        if nicknames is not None and sesame['nickname'] not in nicknames:
            continue
        sesames.append(Sesame(account, sesame))

    return sesames
