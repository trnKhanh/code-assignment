from .base_service import ServiceBase

class ServiceFactory:
  """Factory class to manage all the registered services"""
  registry: dict[str, ServiceBase] = dict()

  @classmethod
  def get_service(cls, service_name: str) -> ServiceBase:
    """Get service by name"""
    if service_name in cls.registry:
      return cls.registry[service_name]
    raise KeyError(f"{service_name}: service not found")

  @classmethod
  def get_all_services(cls):
    """Get all services' names"""
    return cls.registry.keys()

  @classmethod
  def register(cls, service_name: str):
    """Decorator function to register service"""
    def decorator(service):
      cls.registry[service_name] = service

    return decorator