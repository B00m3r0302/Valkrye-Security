## main.py
from database import Database
from logger import Logger
from ui import UI
from file_scanner import FileScanner
from registry_scanner import RegistryScanner
from account_scanner import AccountScanner
from connection_scanner import ConnectionScanner
from typing import Dict, Any
import sys

class Main:
    def __init__(self):
        self.database = Database()
        self.logger = Logger()
        self.ui = UI()
        self.file_scanner = FileScanner()
        self.registry_scanner = RegistryScanner()
        self.account_scanner = AccountScanner()
        self.connection_scanner = ConnectionScanner()

    def run(self) -> None:
        self.ui.show()
        self.scan_system()
        sys.exit(self.ui.app.exec_())

    def scan_system(self) -> None:
        self.ui.update("Scanning files...")
        self.scan_and_compare(self.file_scanner, "files")
        self.ui.update("Scanning registry...")
        self.scan_and_compare(self.registry_scanner, "registry")
        self.ui.update("Scanning accounts...")
        self.scan_and_compare(self.account_scanner, "accounts")
        self.ui.update("Scanning connections...")
        self.scan_and_compare(self.connection_scanner, "connections")
        self.ui.update("Scan completed.")

    def scan_and_compare(self, scanner: Any, table: str) -> None:
        old_data = self.database.query(table)
        new_data = scanner.scan()
        self.database.insert({"table": table, "data": new_data})
        discrepancies = scanner.compare(old_data, new_data)
        if discrepancies:
            self.logger.log(f"Discrepancies found in {table}: {discrepancies}")
            self.ui.alert(f"Discrepancies found in {table}: {discrepancies}")


if __name__ == "__main__":
    main = Main()
    main.run()
