from database import Database
from logger import Logger
from scanner import Scanner
from discrepancy_detector import DiscrepancyDetector
from discrepancy_handler import DiscrepancyHandler
from console_interface import ConsoleInterface

class Main:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.database = Database(self.database_path)
        self.logger = Logger('mchammer.log')
        self.scanner = Scanner()
        self.discrepancy_detector = DiscrepancyDetector(self.database)
        self.discrepancy_handler = DiscrepancyHandler(self.database, self.logger)
        self.console_interface = ConsoleInterface(self.database, self.logger)

    def run(self):
        self.database.create_tables()
        system_info = self.scanner.scan_system()
        for key, value in system_info.items():
            self.database.insert_data('system_info', {'info_type': key, 'info_value': value})
        file_info = self.scanner.scan_files()
        for info in file_info:
            self.database.insert_data('file_info', info)
        user_info = self.scanner.scan_users()
        for info in user_info:
            self.database.insert_data('user_info', info)
        autorun_info = self.scanner.scan_autoruns()
        for info in autorun_info:
            self.database.insert_data('autorun_info', info)
        connection_info = self.scanner.scan_connections()
        for info in connection_info:
            self.database.insert_data('connection_info', info)
        discrepancies = self.discrepancy_detector.detect_discrepancies()
        self.discrepancy_handler.handle_discrepancies(discrepancies)
        self.console_interface.run_menu()

if __name__ == '__main__':
    main = Main('mchammer.db')
    main.run()
