from typing import Any

from datatype import Amenities, Hotel, Images, Location
from utils import remove_none, normalize_string, normalize_float, normalize_int, get_country_name

from .factory import ServiceFactory
from .base_service import ServiceBase


@ServiceFactory.register("acme")
class ACME(ServiceBase):

  @classmethod
  def endpoint(cls) -> str:
    return "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme"

  @classmethod
  def parse(cls, data: dict[str, Any]) -> Hotel | None:
    id = normalize_string(data.get("Id"))
    destination_id = normalize_int(data.get("DestinationId"))
    if id is None or destination_id is None:
      return None
    name = normalize_string(data.get("Name"))
    location = cls.__parse_location(data)
    description = normalize_string(data.get("Description"))
    amenities = cls.__parse_amenities(data)
    images = cls.__parse_images(data)
    booking_conditions = []  # ACME does not have booking conditions field

    return Hotel(id, destination_id, name, location, description, amenities,
                 images, booking_conditions)

  @classmethod
  def __parse_location(cls, data):
    lat = normalize_float(data.get("Latitude"))
    lng = normalize_float(data.get("Longitude"))

    # Construct the address based on Address and PostalCode
    address = normalize_string(data.get("Address"))
    postal_code = normalize_string(data.get("PostalCode"))
    if address and postal_code:
      address = f"{address}, {postal_code}"

    city = normalize_string(data.get("City"))
    country = get_country_name(normalize_string(data.get("Country")))

    location = Location(lat, lng, address, city, country)
    return location

  @classmethod
  def __parse_amenities(cls, data):

    def parse_facility(facility: str):
      try:
        normalized_facility = normalize_string(facility)
        if normalized_facility is None:
          return None

        words = []
        for c in normalized_facility:
          if c.isupper():
            words.append(c.lower())
          else:
            if len(words) == 0:
              words.append("")
            words[-1] += c
        return " ".join(words)
      except Exception:
        return None

    # ACME only have the Facilities field, so we set it to general by default
    general = [parse_facility(x) for x in data.get("Facilities") or []]
    general = remove_none(general)
    amenities = Amenities(general=general)
    return amenities

  @classmethod
  def __parse_images(cls, data):
    # ACME does not have images field
    images = Images()
    return images
