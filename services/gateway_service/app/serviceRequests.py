import requests


def get(url: str, headers: dict = {}, data: dict = {}, timeout=5):
    try:
        return requests.get(url, headers=headers, data=data, timeout=timeout)
    except Exception as e:
        print("Exception in GET method: ", e)
        return None


def post(url: str, headers: dict = {}, data: dict = {}, timeout=5):
    try:
        return requests.post(url, headers=headers, data=data, timeout=timeout)
    except Exception as e:
        print("Exception in POST method: ", e)
        return None


def patch(url: str, headers: dict = {}, data: dict = {}, timeout=5):
    try:
        return requests.patch(url, headers=headers, data=data, timeout=timeout)
    except Exception as e:
        print("Exception in PATCH method: ", e)
        return None
