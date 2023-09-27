## connection_scanner.py
try:
    import psutil
except ImportError as e:
    print(f"Error occurred during psutil module import: {str(e)}")
    sys.exit(1)

import difflib
from typing import Dict, List
from logger import Logger

class ConnectionScanner:
    def __init__(self):
        self.logger = Logger()

    def scan(self) -> Dict[str, str]:
        connections = {}
        try:
            for conn in psutil.net_connections():
                if conn.status == 'ESTABLISHED':
                    connections[f"{conn.laddr.ip}:{conn.laddr.port}"] = f"{conn.raddr.ip}:{conn.raddr.port}"
        except Exception as e:
            self.logger.log(f"Error occurred during connection scan: {str(e)}")
        return connections

    def compare(self, old: Dict[str, str], new: Dict[str, str]) -> List[str]:
        diff = difflib.unified_diff(
            [f"{k} {v}\n" for k, v in old.items()],
            [f"{k} {v}\n" for k, v in new.items()]
        )
        return [line for line in diff if line.startswith('+') or line.startswith('-')]

    def disconnect(self, connections: List[str]) -> None:
        for connection in connections:
            try:
                ip, port = connection.split(':')
                for conn in psutil.net_connections():
                    if conn.laddr == (ip, int(port)):
                        psutil.Process(conn.pid).terminate()
            except Exception as e:
                self.logger.log(f"Error occurred during connection termination: {str(e)}")
