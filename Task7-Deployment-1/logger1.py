import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api.log"),      # writes to a rolling text file
        logging.StreamHandler(sys.stdout)    # also shows logs in the console
    ],
)

logger = logging.getLogger(__name__)
