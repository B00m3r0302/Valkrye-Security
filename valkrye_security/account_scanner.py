## account_scanner.py
import subprocess
import difflib
from typing import Dict, List
from logger import Logger

class AccountScanner:
    def __init__(self):
        self.logger = Logger()

    def scan(self) -> Dict[str, str]:
        accounts = {}
        try:
            proc = subprocess.Popen(['net', 'user'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = proc.communicate()
            if output:
                lines = output.decode('utf-8', errors='ignore').split('\n')
                for line in lines[4:-2]:  # Skip the header and footer lines
                    account = line.strip()
                    if account:
                        accounts[account] = self.get_account_info(account)
        except Exception as e:
            self.logger.log(f"Error occurred during account scan: {str(e)}")
        return accounts

    def get_account_info(self, account: str) -> str:
        try:
            proc = subprocess.Popen(['net', 'user', account], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = proc.communicate()
            if output:
                return output.decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.log(f"Error occurred during account info retrieval: {str(e)}")
        return ""

    def compare(self, old: Dict[str, str], new: Dict[str, str]) -> List[str]:
        diff = difflib.unified_diff(
            [f"{k} {v}\n" for k, v in old.items()],
            [f"{k} {v}\n" for k, v in new.items()]
        )
        return [line for line in diff if line.startswith('+') or line.startswith('-')]

    def delete_accounts(self, accounts: List[str]) -> None:
        for account in accounts:
            try:
                subprocess.call(['net', 'user', account, '/delete'])
            except Exception as e:
                self.logger.log(f"Error occurred during account deletion: {str(e)}")
