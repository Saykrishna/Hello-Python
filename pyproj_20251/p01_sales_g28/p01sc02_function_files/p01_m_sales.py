import decimal
from decimal import Decimal, ROUND_HALF_UP
import locale as lc
import csv
from datetime import datetime, date
from pathlib import Path
from p01sc04_exception_libraries_3tier import p01beg_1da_sales as sd

lc.setlocale(lc.LC_ALL, 'en_US.UTF-8')
FILEPATH = Path(__file__).parent.parent / 'p01_files'
SALES_ID = {"Sales": 1}

# Constants
FILEPATH = Path(__file__).parent.parent / 'p01_files'  # Adjust to your directory path
IMPORTED_FILES = 'imported_files.txt'
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"  # Define naming convention
DATE_FORMAT = "%Y-%m-%d"
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
MIN_YEAR = 2000
MAX_YEAR = 2999

# Function to format currency
def format_currency(amount):
    return lc.currency(decimal.Decimal(amount), grouping=True)

# Function to read sales data from a file
def read_sales_data(filename):
    sales_data = []
    filepath = FILEPATH / filename
    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['amount'] = decimal.Decimal(row['amount'])
                row['sales_date'] = date.fromisoformat(row['date'])
                row['quarter'] = (row['sales_date'].month - 1) // 3 + 1
                sales_data.append(row)
    except FileNotFoundError:
        print(f"FileNotFoundError: Failed to import sales from '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return sales_data
    def view_sales(sales_list: SalesList) -> bool:
        """Display the sales data in a formatted table."""
        bad_data_flag = False

        if sales_list.count == 0: 
            print("No sales to view.")
        else:  
            # Define column widths for the table
            col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15
            total_w = col1_w + col2_w + col3_w + col4_w + col5_w
            print(f"{' ':{col1_w}}"
                  f"{'Date':{col2_w}}"
                  f"{'Quarter':{col3_w}}"
                  f"{'Region':{col4_w}}"
                  f"{'Amount':>{col5_w}}")
            print(horizontal_line := f"{'-' * total_w}")
            total = Decimal('0.0')  # Initialize total amount

            for idx in range(1, sales_list.count + 1):  
                sales = sales_list[idx - 1]
                if sales.has_bad_data:
                    bad_data_flag = True
                    num = f"{idx}.*"  # Mark rows with bad data
                else:
                    num = f"{idx}."

                # Format amount
                amount = sales.amount
                if not sales.has_bad_amount:
                    total += Decimal(str(amount))
                    amount = lc.currency(amount, grouping=True)

                # Format date and calculate quarter
                sales_date = sales.sales_date
                if sales.has_bad_date:
                    bad_data_flag = True
                    month = 0
                else:
                    sales_date = f"{sales_date:{Sales.DATE_FORMAT}}"
                    month = sales.sales_date.month

                region = sales.region.name
                quarter = f"{Sales.cal_quarter(month)}"
                print(f"{num:<{col1_w}}"
                      f"{sales_date:{col2_w}}"
                      f"{quarter:<{col3_w}}"
                      f"{region:{col4_w}}"
                      f"{amount:>{col5_w}}")

            print(horizontal_line)
            total = total.quantize(Decimal("1.00"), ROUND_HALF_UP)
            total = lc.currency(total, grouping=True)
            print(f"{'TOTAL':{col1_w}}"
                  f"{' ':{col2_w + col3_w + col4_w}}"
                  f"{total:>{col5_w}}\n")
            print(f"view_sales: {DataFileAccess.SALES_ID['Sales']=}")
            return bad_data_flag





# Functions for adding sales data
def input_amount() -> decimal.Decimal:
    while True:
        try:
            amount = decimal.Decimal(input(f"{'Amount:':20}"))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")
        except decimal.InvalidOperation:
            print("Invalid input. Please enter a valid amount.")

def input_date() -> date:
    while True:
        try:
            date_str = input(f"{'Date (YYYY-MM-DD):':20}").strip()
            sales_date = datetime.strptime(date_str, DATE_FORMAT).date()
            if sales_date.year < 2000 or sales_date.year > 2999:
                print(f"Year must be between 2000 and 2999.")
            else:
                return sales_date
        except ValueError:
            print(f"{date_str} is not in a valid date format.")
           #print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def input_region_code() -> str:
    while True:
        region_code = input(f"{'Region (w, m, c, e):':20}").strip().lower()
        if region_code in VALID_REGIONS:
            return region_code
        else:
            print(f"Region must be one of the following: {tuple(VALID_REGIONS.keys())}")

class InvalidYearError(Exception):
    pass

class InvalidMonthError(Exception):
    pass

class InvalidDayError(Exception):
    pass

from datetime import date

# Define custom exceptions for each part of the date
class InvalidYearError(Exception):
    pass

class InvalidMonthError(Exception):
    pass

class InvalidDayError(Exception):
    pass

def add_sale_by_components(sales_data):
    # Input for amount
    amount = input_amount()
    
    # Initialize variables for year, month, and day
    year, month, day = None, None, None

    # Loop until a valid year is entered
    while True:
        try:
            # Input for year
            year = int(input("Year: "))
            if year < 2000 or year > 2999:
                raise InvalidYearError("Year must be between 2000 and 2999.")
            break  # If valid year, break the loop

        except InvalidYearError as e:
            print(f"Error: {e}. Please enter a valid year.")
        except ValueError:
            print("Error: Invalid input. Please enter a numerical value for the year.")

    # Loop until a valid month is entered
    while True:
        try:
            # Input for month
            month = int(input("Month: "))
            if month < 1 or month > 12:
                raise InvalidMonthError("Month must be between 1 and 12.")
            break  # If valid month, break the loop

        except InvalidMonthError as e:
            print(f"Error: {e}. Please enter a valid month.")
        except ValueError:
            print("Error: Invalid input. Please enter a numerical value for the month.")
    
    # Loop until a valid day is entered
    while True:
        try:
            # Input for day
            day = int(input("Day: "))
            if day < 1 or day > 28:  # We can allow up to 28 for simplicity
                raise InvalidDayError("Day must be between 1 and 28.")
            break  # If valid day, break the loop

        except InvalidDayError as e:
            print(f"Error: {e}. Please enter a valid day.")
        except ValueError:
            print("Error: Invalid input. Please enter a numerical value for the day.")

    # Create the date object after all parts are validated
    sales_date = date(year, month, day)

    # Input for region code
    region_code = input_region_code()

    # Append the sale data to the list
    sales_data.append({
        "amount": amount,
        "sales_date": sales_date,
        "region": region_code,
        "quarter": (sales_date.month - 1) // 3 + 1  # Calculate quarter
    })

    # Print success message
    print(f"Sales for {sales_date} added.")


def add_sale_by_date(sales_data):
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()
    sales_data.append({
        "amount": amount,
        "sales_date": sales_date,
        "region": region_code,
        "quarter": (sales_date.month - 1) // 3 + 1
    })
    print(f"Sales for {sales_date} added.")

def get_region_code(filename: str) -> str:
    return filename[filename.rfind('.') - 1]

def is_valid_filename_format(filename: str) -> bool:
    if len(filename) == len(NAMING_CONVENTION) and \
       filename[:7] == NAMING_CONVENTION[:7] and \
       filename[8] == NAMING_CONVENTION[8] and \
       filename[13] == NAMING_CONVENTION[13] and \
       filename[-4:] == NAMING_CONVENTION[-4:]:
        return True
    return False

# Function to check if a filename follows the naming convention
def is_valid_filename_format(filename: str) -> bool:
    if len(filename) == len(NAMING_CONVENTION) and \
       filename[:7] == NAMING_CONVENTION[:7] and \
       filename[8] == NAMING_CONVENTION[8] and \
       filename[13] == NAMING_CONVENTION[-6] and \
       filename[-4:] == NAMING_CONVENTION[-4:]:
        return True
    return False

# Function to check if a file has already been imported
def already_imported(filepath_name: Path) -> bool:
    imported_files_path = FILEPATH / IMPORTED_FILES
    try:
        # Read the list of already imported files
        if imported_files_path.exists():
            with open(imported_files_path, 'r') as file:
                files = [line.strip() for line in file.readlines()]
            # Check if the file path already exists in the list
            return str(filepath_name) in files
        else:
            return False
    except FileNotFoundError:
        print(f"File not found: {imported_files_path}")
        return False
    except Exception as e:
        print(f"An error occurred while checking if file was imported: {e}")
        return False

# Function to add a file to the list of already imported files
def add_imported_file(filepath_name: Path):
    imported_files_path = FILEPATH / IMPORTED_FILES
    try:
        # Add the file path to the imported files list
        with open(imported_files_path, 'a') as file:
            file.write(f"{filepath_name}\n")
    except Exception as e:
        print(f"An error occurred while adding to imported files: {e}")

# Function to read and import sales data from a CSV file
def import_sales(filepath_name: Path, delimiter: str = ',') -> list:
    sales_data = []
    try:
        # Check if the file was already imported
        if already_imported(filepath_name):
            print(f"File '{filepath_name}' has already been imported.")
            return sales_data  # Return empty if already imported

        with open(filepath_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            filename = filepath_name.name
            region_code = get_region_code(filename)  # Assumed function to get region from filename

            for row in reader:
                if row:
                    # Assuming 'correct_data_types' is a function to validate row content (you can define it yourself)
                    correct_data_types(row)
                    amount, sales_date = row[0], row[1]
                    data = {"amount": amount,
                            "sales_date": sales_date,
                            "region": region_code}
                    sales_data.append(data)
            
            # Add the file to the list of already imported files
            add_imported_file(filepath_name)
            
    except FileNotFoundError:
        print(f"<class 'FileNotFoundError'>. Failed to import sales from '{filepath_name}'")
    except Exception as e:
        print(f"An error occurred while importing sales data: {e}")
    
    return sales_data

# Helper function to extract region from filename
def get_region_code(filename: str) -> str:
    # Extract the region code (assuming it's the second-to-last character in the file name)
    return filename[filename.rfind('.') - 1] if '.' in filename else 'unknown'

# Placeholder for correct_data_types function
def correct_data_types(row):
    # Example: Ensure that the amount is a valid decimal and the sales_date is in correct format
    try:
        amount = float(row[0])
        sales_date = date.fromisoformat(row[1])  # Assuming date is in 'YYYY-MM-DD' format
    except ValueError:
        print(f"Invalid data in row: {row}. Please check the format.")
        raise ValueError("Incorrect data format")

