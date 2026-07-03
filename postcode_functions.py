"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.

    with open(CACHE_FILE, "r", encoding="utf-8") as cache:
        postcode_data = json.load(cache)

    return postcode_data


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)


def validate_postcode(postcode: str) -> bool:
    """Ensures the postcode is valid."""

    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    cache = load_cache()

    if postcode in cache:
        if 'valid' in cache[postcode]:
            return cache[postcode]['valid']

    res = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate")

    if res.status_code == 200:
        # print(type(res.json()['result']))
        cache[postcode]['valid'] = res.json()['result']
        save_cache(cache)
        return res.json()['result']

    if res.status_code == 500:
        raise req.RequestException("Unable to access API.")


def get_postcode_for_location(lat: float, long: float) -> str:
    """Finds location by latitude and longitude."""

    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    res = req.get(f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}")

    if res.status_code == 200:

        if res.json()['result'] == None:
            raise ValueError("No relevant postcode found.")

        return res.json()['result'][0]['postcode']

    if res.status_code == 500:
        raise req.RequestException("Unable to access API.")


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Completes the postcode."""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    res = req.get(
        f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete")

    if res.status_code == 200:

        return res.json()['result']

    if res.status_code == 500:
        raise req.RequestException("Unable to access API.")


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns the details attached to the postcode."""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for item in postcodes:
        if not isinstance(item, str):
            raise TypeError("Function expects a list of strings.")

    postcode_dict = {}
    postcode_dict['postcodes'] = postcodes
    postcodes_json = json.dumps(postcode_dict)

    res = req.post(f"https://api.postcodes.io/postcodes", json=postcodes_json)

    if res.status_code == 200:

        return res.json()['result']

    if res.status_code == 500:
        raise req.RequestException("Unable to access API.")


if __name__ == "__main__":
    validate_postcode("E79FG")
