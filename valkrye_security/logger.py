import logging
from typing import Any

class Logger:
    def __init__(self, log_file: str = "valkrye_security.log"):
        try:
            logging.basicConfig(filename=log_file, level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
        except Exception as e:
            print(f"Error occurred during logger setup: {str(e)}")

    def log(self, message: Any) -> None:
        try:
            logging.info(message)
        except Exception as e:
            print(f"Error occurred during logging: {str(e)}")
