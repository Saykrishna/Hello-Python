import sqlite3
from pathlib import Path
from datetime import date
from typing import Optional

# Define the Sales and Region classes
class Sales:
    def __init__(self, id: int, amount: float, sales_date: date, region: str):
        self.id = id
        self.amount = amount
        self.sales_date = sales_date
        self.region = region

class Region:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

class SQLiteDBAccess:
    SQLITEDBPATH = Path(__file__).parent.parent / 'p01_db'

    def __init__(self):
        self._sqlite_sales_db = 'sales_db.sqlite'
        self._dbpath_sqlite_sales_db = SQLiteDBAccess.SQLITEDBPATH / self._sqlite_sales_db

    def connect(self) -> sqlite3.Connection:
        '''Connect to the SQLite database and return the connection object.'''
        try:
            conn = sqlite3.connect(self._dbpath_sqlite_sales_db)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        '''Retrieve ID, amount, salesDate, and region field from Sales table for the records 
        that have the given salesDate and region values.'''
        query = '''
            SELECT id, amount, salesDate, region
            FROM Sales
            WHERE salesDate = ? AND region = ?
        '''
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, (sales_date, region_code))
            result = cursor.fetchone()
            if result:
                id, amount, sales_date, region_code = result
                return Sales(id, amount, sales_date, region_code)
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving sales data: {e}")
            return None
        finally:
            conn.close()

    def update_sales(self, sales: Sales) -> None:
        '''Update amount, salesDate, and region fields of Sales table for the record with the given ID value.'''
        query = '''
            UPDATE Sales
            SET amount = ?, salesDate = ?, region = ?
            WHERE id = ?
        '''
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, (sales.amount, sales.sales_date, sales.region, sales.id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating sales data: {e}")
        finally:
            conn.close()

    def retrieve_regions(self) -> list[Region]:
        '''Retrieve region code and name from Region table.'''
        query = '''
            SELECT code, name
            FROM Region
        '''
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            regions = [Region(*row) for row in rows]  # assuming Region constructor accepts these values
            return regions
        except sqlite3.Error as e:
            print(f"Error retrieving regions: {e}")
            return []
        finally:
            conn.close()


