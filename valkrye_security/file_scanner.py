## file_scanner.py

import os
import hashlib
from typing import Dict, List


class FileScanner:
    def __init__(self, directory: str = "c:\\"):
        self.directory = directory

    def scan(self) -> Dict[str, str]:
        files = {}
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as file:
                        files[filepath] = hashlib.md5(file.read()).hexdigest()
        return files

    def compare(self, old: Dict[str, str], new: Dict[str, str]) -> List[str]:
        added = [file for file in new if file not in old]
        removed = [file for file in old if file not in new]
        changed = [file for file in new if file in old and new[file] != old[file]]
        return added + removed + changed

    def delete_executables(self, files: List[str]) -> None:
        for file in files:
            if file.endswith(('.exe', '.dll', '.sys')):
                try:
                    os.remove(file)
                except PermissionError:
                    print(f"Permission denied: '{file}'")
                except OSError as e:
                    print(f"Error: '{file}': {str(e)}")
