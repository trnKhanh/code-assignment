from dataclasses import dataclass, field

from utils import get_longest_string


@dataclass
class Location:
  lat: float | None = None
  lng: float | None = None
  address: str | None = None
  city: str | None = None
  country: str | None = None

  def merge(self, other: "Location") -> "Location":
    lat = self.lat or other.lat
    lng = self.lng or other.lng
    address = self.address or other.address
    city = self.city or other.city
    country = self.country or other.country
    return Location(lat, lng, address, city, country)


@dataclass
class Amenities:
  general: list[str] = field(default_factory=list[str])
  room: list[str] = field(default_factory=list[str])

  def merge(self, other: "Amenities") -> "Amenities":
    # The merge function of amenities could be over-complicated since the data
    # from some suppliers are not unified (e.g. wifi 
    # and WiFi-parsed to wi fi-are refered to the same thing)
    def merge_list(l1, l2):
      """Merge two lists of amenities"""
      # Two amenity is considered the same if its key_fn value is the same
      # (e.g. wifi and wi fi are the same)
      res = []
      def key_fn(x):
        return x.replace(" ", "").lower()
        
      sorted_list = sorted(l1 + l2, key=lambda x: (key_fn(x), len(x)))
      for s in sorted_list:
        if len(res) == 0 or key_fn(res[-1]) != key_fn(s):
          res.append(s)
      return res
      
    general = merge_list(self.general, other.general)
    room = merge_list(self.room, other.room)
    return Amenities(general, room)


@dataclass
class ImageInfo:
  link: str
  description: str | None = None

  def merge(self, other: "ImageInfo") -> "ImageInfo":
    if self.link != other.link:
      raise ValueError("Link must be the same to merge ImageInfo")

    link = self.link
    description = self.description or other.description
    
    return ImageInfo(link, description)


@dataclass
class Images:
  rooms: list[ImageInfo] = field(default_factory=list[ImageInfo])
  site: list[ImageInfo] = field(default_factory=list[ImageInfo])
  amenities: list[ImageInfo] = field(default_factory=list[ImageInfo])

  def merge(self, other: "Images") -> "Images":
    def merge_images_set(s1, s2):
      """Merge two sets of images"""
      S = sorted(s1 + s2, key=lambda x: x.link)
      res = []
      for x in S:
        try:
          res[-1] = res[-1].merge(x)
        except Exception:
          res.append(x)
      return res

    rooms = merge_images_set(self.rooms, other.rooms)
    site = merge_images_set(self.site, other.site)
    amenities = merge_images_set(self.amenities, other.amenities)
    return Images(rooms, site, amenities)


@dataclass
class Hotel:
  id: str
  destination_id: int
  name: str | None = None
  location: Location = field(default_factory=Location)
  description: str | None = None
  amenities: Amenities = field(default_factory=Amenities)
  images: Images = field(default_factory=Images)
  booking_conditions: list[str] = field(default_factory=list[str])

  def merge(self, other: "Hotel") -> "Hotel":
    if self.id != other.id or self.destination_id != other.destination_id:
      raise ValueError("Hotel IDs must be the same to merge Hotel")
      
    id = self.id
    destination_id = self.destination_id

    # Merge fields that are default types (str, list, e.t.c.)
    name = self.name or other.name
    description = get_longest_string(
      self.description, other.description)  # prefer longer description
    booking_conditions = list(set().union(self.booking_conditions,
      other.booking_conditions))
    
    # Merge fields that are defined dataclasses
    location = self.location.merge(other.location)
    amenities = self.amenities.merge(other.amenities)
    images = self.images.merge(other.images)
  
    return Hotel(id, destination_id, name, location, description, amenities,
                 images, booking_conditions)
