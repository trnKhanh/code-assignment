from typing import Any

from datatype import Amenities, Hotel, ImageInfo, Images, Location
from utils import remove_none, normalize_string, normalize_float, normalize_int

from .factory import ServiceFactory
from .base_service import ServiceBase


@ServiceFactory.register("patagonia")
class Patagonia(ServiceBase):

  @classmethod
  def endpoint(cls) -> str:
    return "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia"

  @classmethod
  def parse(cls, data: dict[str, Any]) -> Hotel | None:
    id = normalize_string(data.get("id"))
    destination_id = normalize_int(data.get("destination"))
    if id is None or destination_id is None:
      return None
    name = normalize_string(data.get("name"))
    location = cls.__parse_location(data)
    description = normalize_string(data.get("info"))
    amenities = cls.__parse_amenities(data)
    images = cls.__parse_images(data)

    booking_conditions = cls.__parse_booking_conditions(data)

    return Hotel(id, destination_id, name, location, description, amenities,
                 images, booking_conditions)

  @classmethod
  def __parse_booking_conditions(cls, data):
    booking_conditions = [
        normalize_string(c) for c in data.get("booking_conditions") or []
    ]
    booking_conditions = remove_none(booking_conditions)
    return booking_conditions

  @classmethod
  def __parse_location(cls, data):
    lat = normalize_float(data.get("lat"))
    lng = normalize_float(data.get("lng"))
    address = normalize_string(data.get("address"))
    city = None
    country = None

    location = Location(lat, lng, address, city, country)
    return location

  @classmethod
  def __parse_amenities(cls, data):

    def parse_facility(facility: str):
      try:
        normalized_facility = normalize_string(facility)
        if normalized_facility is None:
          return None
        return normalized_facility.lower()
      except Exception:
        return None

    # Patagonia only have the Facilities field, so we set it to room by default
    general = []
    room = [parse_facility(x) for x in data.get("amenities") or []]
    room = remove_none(room)
    amenities = Amenities(general, room)
    return amenities

  @classmethod
  def __parse_images(cls, data):

    def parse_image_info(raw_image_info):
      link = normalize_string(raw_image_info.get("url", None))
      if link is None:
        return None
      description = normalize_string(raw_image_info.get("description", None))
      return ImageInfo(link, description)

    def parse_images_list(images_list):
      try:
        images = [parse_image_info(img) for img in images_list]
        images = remove_none(images)
      except Exception:
        images = []
      return images

    processed_images = {}
    for image_type, raw_images_list in data.get("images", {}).items():
      processed_images[normalize_string(image_type)] = parse_images_list(
          raw_images_list)

    images = Images(**processed_images)
    return images
