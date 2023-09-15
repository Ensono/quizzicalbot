import logging
import uvicorn
from core.config import settings

# Configure format
FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

# create dictionary for the logging level string to the constant
# in the logging module
levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

def init_loggers(logger_name: str = "simple_example"):
    formatter = uvicorn.logging.DefaultFormatter(fmt = FORMAT)

# create the logger
logging.basicConfig(level = levels[settings.log_level])

logger = logging.getLogger(__name__)

# create the logger
# logger = logging.getLogger(__name__)
# logger.setLevel(levels[settings.log_level])

# create console handler
ch = logging.StreamHandler()
ch.setLevel(levels[settings.log_level])

# configure the formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
