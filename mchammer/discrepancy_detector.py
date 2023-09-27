## discrepancy_detector.py
import os
import socket
import hashlib
import psutil
from typing import List, Dict

class DiscrepancyDetector:
    def __init__(self, database):
        self.database = database

    def detect_discrepancies(self) -> List[Dict[str, str]]:
        discrepancies = []
        system_info = self.database.get_data('system_info')
        file_info = self.database.get_data('file_info')
        user_info = self.database.get_data('user_info')
        autorun_info = self.database.get_data('autorun_info')
        connection_info = self.database.get_data('connection_info')

        # Detect discrepancies in system info
        for info in system_info:
            if info['info_type'] == 'os' and info['info_value'] != os.name:
                discrepancies.append({'type': 'system_info', 'detail': f"OS changed from {info['info_value']} to {os.name}"})
            elif info['info_type'] == 'hostname' and info['info_value'] != socket.gethostname():
                discrepancies.append({'type': 'system_info', 'detail': f"Hostname changed from {info['info_value']} to {socket.gethostname()}"})
            elif info['info_type'] == 'os_version' and info['info_value'] != os.uname().release:
                discrepancies.append({'type': 'system_info', 'detail': f"OS version changed from {info['info_value']} to {os.uname().release}"})

        # Detect discrepancies in file info
        for info in file_info:
            try:
                with open(info['file_path'], 'rb') as f:
                    bytes = f.read()
                    readable_hash = hashlib.sha256(bytes).hexdigest()
                    if readable_hash != info['file_hash']:
                        discrepancies.append({'type': 'file_info', 'detail': f"File {info['file_path']} hash changed from {info['file_hash']} to {readable_hash}"})
            except Exception as e:
                discrepancies.append({'type': 'file_info', 'detail': f"File {info['file_path']} not found"})

        # Detect discrepancies in user info
        current_users = psutil.users()
        for info in user_info:
            if not any(user.name == info['user_name'] and user.uid == info['user_id'] for user in current_users):
                discrepancies.append({'type': 'user_info', 'detail': f"User {info['user_name']} not found"})

        # Detect discrepancies in autorun info
        # Removed dependency on 'autorunsc.exe'

        # Detect discrepancies in connection info
        current_connections = psutil.net_connections()
        for info in connection_info:
            if not any(conn.laddr == info['local_address'] and conn.raddr == info['remote_address'] and conn.status == info['status'] for conn in current_connections):
                discrepancies.append({'type': 'connection_info', 'detail': f"Connection {info['local_address']} to {info['remote_address']} not found"})

        return discrepancies
