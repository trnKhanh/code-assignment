from argparse import ArgumentParser
import json

from utils import parse_hotel_ids, parse_destination_ids, JSONDataclassEncoder
from logger import logger
from processor import Processor

def main(args):
  # Parse the input hotel and destination IDs
  args.hotel_ids = parse_hotel_ids(args.hotel_ids)
  args.destination_ids = parse_destination_ids(args.destination_ids)

  logger.info(f"Hotel IDs: {args.hotel_ids}")
  logger.info(f"Destination IDs: {args.destination_ids}")

  # Init the processor
  processor = Processor()
  # Run the processor to (1) fetch hotels data, (2) process data (dependant
  # on the supplier), (3) filter data, and (4) merge data
  data = processor.run(args.hotel_ids, args.destination_ids)

  # Print data in json format to stdout
  print(json.dumps(data, cls=JSONDataclassEncoder, indent=1))


def create_args():
  parser = ArgumentParser()

  parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
  parser.add_argument("destination_ids", type=str, help="Destination IDs")

  return parser.parse_args()


if __name__ == "__main__":
  args = create_args()
  main(args)
