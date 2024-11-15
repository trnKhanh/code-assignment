from typing import Any
from datatype import Hotel
from services import ServiceFactory
from logger import logger

class Processor:
  """Processor class to fetch and process hotels data. If the suppliers list are not provided then it will fetch data from all suppliers."""
  def __init__(self, service_names: str | None = None):
    if service_names is not None:
      self.service_names = service_names
    else:
      self.service_names = ServiceFactory.get_all_services()
  
  def fetch(self) -> dict[str, Any]:
    """Fetch data from supplier."""
    raw_data = {}
    for name in self.service_names:
      raw_data[name] = ServiceFactory.get_service(name).fetch()

    return raw_data

  def parse(self, raw_data: dict[str, Any]) -> list[Hotel]:
    """Parse data from suppliers"""
    data = []
    for name, hotels in raw_data.items():
      for raw_hotel in hotels:
        data.append(ServiceFactory.get_service(name).parse(raw_hotel))
    return data

  def merge(self, data: list[Hotel]):
    """Merge hotels lists"""
    sorted_data = sorted(data, key=lambda x: (x.id, x.destination_id))
    merged_data = []
    for x in sorted_data:
      try:
        merged_data[-1] = merged_data[-1].merge(x)
      except Exception as e:
        merged_data.append(x)
    return merged_data

  def filter(self, data: list[Hotel], hotel_ids: list[str] | None, destination_ids: list[int] | None):
    """Filter out hotels that are not in the provided hotel_ids and destination_ids."""
    filtered_data = []
    for hotel in data:
      if hotel_ids and hotel.id not in hotel_ids:
        continue
      if destination_ids and hotel.destination_id not in destination_ids:
        continue
      filtered_data.append(hotel)
    return filtered_data

  def run(self, hotel_ids: list[str] | None, destination_ids: list[int] | None):
    """Run all the steps"""
    raw_data = self.fetch()
    data = self.parse(raw_data)
    
    if hotel_ids or destination_ids:
      filtered_data = self.filter(data, hotel_ids, destination_ids)
    else:
      filtered_data = data
      
    merged_data = self.merge(filtered_data)
    return merged_data