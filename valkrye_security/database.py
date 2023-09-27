## database.py

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict

class Database:
    def __init__(self, db_url: str = "sqlite:///valkrye_security.db"):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, data: Dict[str, Any]) -> None:
        session = self.Session()
        try:
            table_name = data.pop("table")
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            session.execute(table.insert(), data)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Error occurred during insertion: {str(e)}")
        finally:
            session.close()

    def query(self, table_name: str) -> Any:
        session = self.Session()
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            result = session.execute(table.select()).fetchall()
            return result
        except SQLAlchemyError as e:
            print(f"Error occurred during query: {str(e)}")
        finally:
            session.close()
