## database.py
import sqlite3
from typing import Dict
from contextlib import closing

class Database:
    def __init__(self, database_path: str):
        self.database_path = database_path

    def create_tables(self):
        with closing(sqlite3.connect(self.database_path)) as conn, conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS system_info
                         (info_type TEXT, info_value TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS file_info
                         (file_path TEXT, file_hash TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                         (user_name TEXT, user_id TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS autorun_info
                         (autorun_path TEXT, autorun_hash TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS connection_info
                         (local_address TEXT, remote_address TEXT, status TEXT)''')
            conn.commit()

    def insert_data(self, table: str, data: Dict[str, str]):
        with closing(sqlite3.connect(self.database_path)) as conn, conn.cursor() as cursor:
            placeholders = ', '.join(['?'] * len(data))
            columns = ', '.join(data.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            conn.commit()

    def get_data(self, table: str):
        with closing(sqlite3.connect(self.database_path)) as conn, conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            data = cursor.fetchall()
        return data

    def update_data(self, table: str, data: Dict[str, str]):
        with closing(sqlite3.connect(self.database_path)) as conn, conn.cursor() as cursor:
            columns = ', '.join([f"{k} = ?" for k in data.keys()])
            sql = f"UPDATE {table} SET {columns}"
            cursor.execute(sql, list(data.values()))
            conn.commit()

    def delete_data(self, table: str, data: Dict[str, str]):
        with closing(sqlite3.connect(self.database_path)) as conn, conn.cursor() as cursor:
            placeholders = ' AND '.join([f"{k} = ?" for k in data.keys()])
            sql = f"DELETE FROM {table} WHERE {placeholders}"
            cursor.execute(sql, list(data.values()))
            conn.commit()
