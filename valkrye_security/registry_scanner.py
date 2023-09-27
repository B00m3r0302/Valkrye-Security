## registry_scanner.py
import subprocess
import difflib
from typing import Dict, List
from logger import Logger

class RegistryScanner:
    def __init__(self, registry_path: str = "HKLM\\SOFTWARE"):
        self.registry_path = registry_path
        self.logger = Logger()

    def scan(self) -> Dict[str, str]:
        keys = {}
        try:
            proc = subprocess.Popen(['reg', 'query', self.registry_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = proc.communicate()
            if output:
                lines = output.decode('utf-8', errors='ignore').split('\n')
                for line in lines:
                    if line.startswith(self.registry_path):
                        key = line[len(self.registry_path):].strip()
                        if key:
                            keys[key] = self.get_key_value(key)
        except Exception as e:
            self.logger.log(f"Error occurred during registry scan: {str(e)}")
        return keys

    def get_key_value(self, key: str) -> str:
        try:
            proc = subprocess.Popen(['reg', 'query', f"{self.registry_path}\\{key}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = proc.communicate()
            if output:
                lines = output.decode('utf-8', errors='ignore').split('\n')
                for line in lines:
                    if line.startswith(key):
                        return line[len(key):].strip()
        except Exception as e:
            self.logger.log(f"Error occurred during registry key value retrieval: {str(e)}")
        return ""

    def compare(self, old: Dict[str, str], new: Dict[str, str]) -> List[str]:
        diff = difflib.unified_diff(
            [f"{k} {v}\n" for k, v in old.items()],
            [f"{k} {v}\n" for k, v in new.items()]
        )
        return [line for line in diff if line.startswith('+') or line.startswith('-')]

    def delete_keys(self, keys: List[str]) -> None:
        for key in keys:
            try:
                subprocess.call(['reg', 'delete', f"{self.registry_path}\\{key}", '/f'])
            except Exception as e:
                self.logger.log(f"Error occurred during registry key deletion: {str(e)}")
