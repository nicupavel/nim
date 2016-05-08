import sys
import logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=LOG_FORMAT)
log = logging
