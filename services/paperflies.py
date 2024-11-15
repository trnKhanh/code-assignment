from typing import Any

from datatype import Amenities, Hotel, ImageInfo, Images, Location
from utils import remove_none, normalize_string, normalize_int

from .factory import ServiceFactory
from .base_service import ServiceBase


@ServiceFactory.register("paperflies")
class Paperflies(ServiceBase):

  @classmethod
  def endpoint(cls) -> str:
    return "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies"

  @classmethod
  def parse(cls, data: dict[str, Any]) -> Hotel | None:
    id = normalize_string(data.get("hotel_id"))
    destination_id = normalize_int(data.get("destination_id"))
    if id is None or destination_id is None:
      return None
    name = normalize_string(data.get("hotel_name"))
    location = cls.__parse_location(data)
    description = normalize_string(data.get("details"))
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
    lat = None
    lng = None
    address = None
    city = None
    country = None

    raw_location = data.get("location")
    if raw_location:
      address = normalize_string(raw_location.get("address"))
      country = normalize_string(raw_location.get("country"))

    location = Location(lat, lng, address, city, country)
    return location

  @classmethod
  def __parse_amenities(cls, data):

    def parse_amenities_list(amenities_list):
      amenities = [normalize_string(x) for x in amenities_list]
      amenities = remove_none(amenities)
      return amenities

    process_amenities = {}
    for amenity_type, raw_amenities_list in (data.get("amenities")
                                             or {}).items():
      process_amenities[normalize_string(amenity_type)] = parse_amenities_list(
          raw_amenities_list)

    amenities = Amenities(**process_amenities)
    return amenities

  @classmethod
  def __parse_images(cls, data):

    def parse_image_info(raw_image_info):
      link = normalize_string(raw_image_info.get("link", None))
      if link is None:
        return None
      description = normalize_string(raw_image_info.get("caption", None))
      return ImageInfo(link, description)

    def parse_images_list(images_list):
      try:
        images = [parse_image_info(img) for img in images_list]
        images = remove_none(images)
      except Exception:
        images = []
      return images

    processed_images = {}
    for image_type, raw_images_list in (data.get("images") or {}).items():
      processed_images[normalize_string(image_type)] = parse_images_list(
          raw_images_list)

    images = Images(**processed_images)
    return images
