## scanner.py
import os
import subprocess
import hashlib
import psutil
import socket
from typing import List, Dict


class Scanner:
    def __init__(self):
        pass

    def scan_system(self) -> Dict[str, str]:
        system_info = {
            'os': os.name,
            'hostname': socket.gethostname(),
            'os_version': os.uname().release
        }
        return system_info

    def scan_files(self, directory: str = '/') -> List[Dict[str, str]]:
        file_info = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        bytes = f.read()
                        readable_hash = hashlib.sha256(bytes).hexdigest()
                        file_info.append({'file_path': file_path, 'file_hash': readable_hash})
                except Exception as e:
                    pass
        return file_info

    def scan_users(self) -> List[Dict[str, str]]:
        user_info = []
        for user in psutil.users():
            user_info.append({'user_name': user.name, 'user_id': user.uid})
        return user_info

    def scan_autoruns(self) -> List[Dict[str, str]]:
        autorun_info = []
        # Removed dependency on 'autorunsc.exe'
        return autorun_info

    def scan_connections(self) -> List[Dict[str, str]]:
        connection_info = []
        for conn in psutil.net_connections():
            connection_info.append({'local_address': conn.laddr, 'remote_address': conn.raddr, 'status': conn.status})
        return connection_info
