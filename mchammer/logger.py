## logger.py
import logging

class Logger:
    def __init__(self, log_file: str):
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file, level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_discrepancy(self, discrepancy: str):
        logging.info(discrepancy)
