import requests

def load_input(url=None):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text
