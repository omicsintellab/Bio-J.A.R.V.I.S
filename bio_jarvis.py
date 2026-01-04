import logging
from parse_config import parse_handle

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    parse_handle()
