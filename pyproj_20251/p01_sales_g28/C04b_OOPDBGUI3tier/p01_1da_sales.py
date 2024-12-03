import csv
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from pathlib import Path
from p01sc04_exception_libraries_3tier.p01beg_1da_sales import DataFileAccess, ImportedFile, InputAccess, Regions, Sales, SalesFile, SalesList
from C04b_OOPDBGUI3tier.p01_3gui_tkinter import Regions
from C04b_OOPDBGUI3tier.p01_1da_sales_db import  Region, Sales

# Define classes for Region, Sales, and other data classes...

class DataFileAccess:
    FILEPATH = Path(__file__).parent.parent / 'p01_files'
    SALES_ID = {"Sales": 1}

    def __init__(self, filename: str=""):
        self._ALL_SALES = filename if filename else 'all_sales.csv'
        self._all_sale_filepath_name = DataFileAccess.FILEPATH / self._ALL_SALES
        self._all_sales_list = self.__import_all_sales()

    def __import_all_sales(self) -> SalesList:
        try:
            with open(self._all_sale_filepath_name, newline='') as csvfile:
                reader = csv.reader(csvfile)
                all_sales_list = SalesList()
                for line in reader:
                    if len(line) > 0:
                        *amount_sales_date, region_code = line
                        Sales.correct_data_types(amount_sales_date)
                        amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                        kwarg = {"id": DataFileAccess.SALES_ID["Sales"],
                            "amount": amount,
                            "sales_date": sales_date,
                            "region": Regions().get(region_code),
                        }
                        sales = Sales(**kwarg)
                        all_sales_list.add(sales)
                        DataFileAccess.SALES_ID["Sales"] += 1
                return all_sales_list
        except FileNotFoundError:
            print("Sales file not found.")
            return SalesList()  # Return an empty list if file not found

    def add_sales(self, sales_obj):
        sales_obj["ID"] = DataFileAccess.SALES_ID["Sales"]
        self._all_sales_list.add(sales_obj)
        DataFileAccess.SALES_ID["Sales"] += 1

    def concat_saleslist(self, other_list):
        for sales in other_list:
            sales["ID"] = DataFileAccess.SALES_ID["Sales"]
            DataFileAccess.SALES_ID["Sales"] += 1
        self._all_sales_list.concat(other_list)

    def save_all_sales(self, delimiter: str = ',') -> None:
        # Prepare sales records, excluding sales.id
        sales_records = [[sales.amount, f"{sales.sales_date:{Sales.DATE_FORMAT}}", sales.region.code]
                         for sales in self._all_sales_list]
        
        try:
            with open(self._all_sale_filepath_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter)  # Initialize the writer
                writer.writerow(['Amount', 'Sales Date', 'Region'])  # Optionally add a header row
                writer.writerows(sales_records)  # Write the sales data
                print("Saved sales records.")
        except Exception as e:
            print(type(e), "Sales data could not be saved.")

class Sales:
    DATE_FORMAT = "%Y-%m-%d"            # Class constants
    MIN_YEAR, MAX_YEAR = 2000, 2_999

    def __init__(self, id: int, amount: float=0.0, sales_date: date=None, region: Region=None):
        self._salesdata = {"ID": id, "amount": amount, "salesDate": sales_date, "region": region}

    def __str__(self):
        return (f"Sales(ID={self._salesdata["ID"]}, amount={self._salesdata["amount"]}, "
                f"date={self._salesdata["salesDate"]}, region={self._salesdata["region"]})")

    def __setitem__(self, key, value):
        self._salesdata[key] = value

    @property
    def id(self):
        return self._salesdata["ID"]

    @id.setter
    def id(self, value):
        self._salesdata["ID"] = value

    @property
    def amount(self):
        return self._salesdata["amount"]

    @property
    def sales_date(self):
        return self._salesdata["salesDate"]

    @property
    def region(self):
        return self._salesdata["region"]

    @property
    def has_bad_amount(self) -> bool:
        return self._salesdata["amount"] == "?" # or self.amount <= 0

    @property
    def has_bad_date(self) -> bool:
        return self._salesdata["salesDate"] == "?" # or not isinstance(self.sales_date, date)

    @property
    def has_bad_data(self) -> bool:
        return self.has_bad_amount or self.has_bad_date

    @staticmethod
    def correct_data_types(row):
        try:  # amount
            row[0] = float(row[0]) # convert to float
        except ValueError:
            row[0] = "?"    # Mark invalid amount as bad
        try:  # date
            sales_date = datetime.strptime(row[1], Sales.DATE_FORMAT)
            row[1] = sales_date.date()  # convert to date
        except ValueError:
            row[1] = "?"    # Mark invalid date as bad

    @staticmethod
    def cal_quarter(month: int) -> int:
        if month in (1, 2, 3):
            quarter = 1
        elif month in (4, 5, 6):
            quarter = 2
        elif month in (7, 8, 9):
            quarter = 3
        elif month in (10, 11, 12):
            quarter = 4
        else:
            quarter = 0
        return quarter

    @staticmethod
    def is_leap_year(year: int) -> bool:
        if year % 400 == 0:  # divisible by 400 --> leap year
            return True
        elif year % 100 == 0:  # not divisible by 400, but by 100 --> not leap year
            return False
        elif year % 4 == 0:  # not divisible by 100, but by 4,  --> leap year
            return True
        else:
            return False

    @staticmethod
    def cal_max_day(year: int, month: int) -> int:
        if Sales.is_leap_year(year) and month == 2:  # short-circuit
            return 29
        elif month == 2:
            return 28
        elif month in (4, 6, 9, 11):
            return 30
        else:
            return 31