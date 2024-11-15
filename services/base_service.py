from abc import ABC, abstractmethod

import requests

from datatype import Hotel
from logger import logger


class ServiceBase(ABC):
  """Base class for all services"""

  @classmethod
  @abstractmethod
  def endpoint(cls) -> str:
    """Endpoint for the service"""
    pass

  @classmethod
  def fetch(cls):
    """Fetch data from the endpoint"""
    logger.info(f"Fetching data from {cls.endpoint()}")
    response = requests.get(cls.endpoint())
    if response.ok:
      return response.json()
    else:
      logger.error(
          f"{response.status_code} {response.reason}: Failed to fetch data from {cls.endpoint()}"
      )
      return None

  @classmethod
  @abstractmethod
  def parse(cls, data: dict) -> Hotel | None:
    """Parse data from the supplier"""
    pass
