import logging
import sys
from rich.logging import RichHandler
from rich.console import Console

# Initialize logger using rich handlers
# Log is written to stderr
FORMAT = "%(message)s"
DATE_FORMAT = "YYYY-MM-DD HH:mm:ss"
logging.basicConfig(format=FORMAT,
                    datefmt=DATE_FORMAT,
                    handlers=[
                        RichHandler(console=Console(stderr=True),
                                    rich_tracebacks=True,
                                    show_time=False,
                                    show_path=False)
                    ])

logger = logging.getLogger("hotel_data")
logger.setLevel(logging.INFO)
