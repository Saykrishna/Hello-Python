from pathlib import Path
from datetime import date
import sqlite3
from typing import Optional
from p01sc06_OOPDBGUI3tier.p01beg_1da_sales import Regions, Sales

class SQLiteDBAccess:
    SQLITEDBPATH = Path(__file__).parent.parent / 'p01_db'

    def __init__(self):
        self._sqlite_sales_db = 'sales_db.sqlite'
        self._dbpath_sqlite_sales_db = SQLiteDBAccess.SQLITEDBPATH / self._sqlite_sales_db

    def connect(self) -> sqlite3.Connection:
        '''Connect to the SQLite database and return the connection object.'''
        try:
            connection = sqlite3.connect(self._dbpath_sqlite_sales_db)
            return connection
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
        connection = self.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query, (sales_date, region_code))
            result = cursor.fetchone()
            if result:
                # Assuming Sales class has a suitable constructor to map fields
                return Sales(*result)
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving sales: {e}")
            return None
        finally:
            connection.close()

    def update_sales(self, sales: Sales) -> None:
        '''Update amount, salesDate, and region fields of Sales table for the record with the given ID value.'''
        query = '''
            UPDATE Sales
            SET amount = ?, salesDate = ?, region = ?
            WHERE id = ?
        '''
        connection = self.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query, (sales.amount, sales.sales_date, sales.region, sales.id))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating sales: {e}")
        finally:
            connection.close()

    def retrieve_regions(self) -> Regions:
        '''Retrieve region code and name from Region table.'''
        query = '''
            SELECT region_code, region_name
            FROM Region
        '''
        connection = self.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # Assuming Regions class can be instantiated with a list of tuples (code, name)
            return Regions(results)
        except sqlite3.Error as e:
            print(f"Error retrieving regions: {e}")
            return Regions([])  # Return empty Regions object if error
        finally:
            connection.close()

class Sales:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, id, amount, sales_date, region):
        self.id = id
        self.amount = amount
        self.sales_date = sales_date
        self.region = region

class Regions:
    def __init__(self, region_data):
        # Assuming region_data is a list of tuples (region_code, region_name)
        self.region_data = region_data

    @property
    def codes(self):
        return [region[0] for region in self.region_data]

    @property
    def names(self):
        return [region[1] for region in self.region_data]
