from typing import Any
import json
import dataclasses
import pycountry


def normalize_string(value) -> str | None:
  try:
    return value.strip()
  except Exception:
    return None


def normalize_float(value) -> float | None:
  try:
    return float(value)
  except Exception:
    return None


def normalize_int(value) -> int | None:
  try:
    return int(value)
  except Exception:
    return None


def remove_none(arr) -> list:
  try:
    return [x for x in arr if x is not None]
  except Exception:
    return []


def get_longest_string(*args) -> str | None:
  sorted_list = sorted(remove_none([str(x) for x in args]),
                       key=lambda x: len(x),
                       reverse=True)
  if len(sorted_list):
    return sorted_list[0]
  return None


def parse_hotel_ids(hotel_ids: str) -> list[str] | None:
  if (hotel_ids.lower() == "none"):
    return None

  return hotel_ids.split(",")


def parse_destination_ids(destination_ids: str) -> list[int] | None:
  if (destination_ids.lower() == "none"):
    return None

  return [int(id) for id in destination_ids.split(",")]


def get_country_name(code: str | None):
  if code is None:
    return None

  country = pycountry.countries.get(alpha_2=code)
  if country:
    return country.name
  return None


class JSONDataclassEncoder(json.JSONEncoder):

  def default(self, o: Any) -> Any:
    if dataclasses.is_dataclass(o):
      return dataclasses.asdict(o)
    return super().default(o)
