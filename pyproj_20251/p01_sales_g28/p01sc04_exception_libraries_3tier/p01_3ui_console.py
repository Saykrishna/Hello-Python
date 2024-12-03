import sys
import csv
import os
from pathlib import Path
# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)

# Import the module
from p01sc02_function_files import p01_m_sales



#import sys
#import os
#from pathlib import Path
# Add the root directory to sys.path
#sys.path.append(os.path.abspath(os.getcwd()))

# Now try importing
#from p01sc02_function_files import p01_m_sales

from p01sc02_function_files.p01_m_sales import read_sales_data, view_sales, add_sale_by_components,is_valid_filename_format, add_imported_file, already_imported, add_sale_by_date


# Define the filepath where the sales data files are located
FILEPATH = Path(__file__).parent.parent / 'p01_files'


def import_all_sales(sales_data: list, file_path: Path) -> bool:
    """
    Imports sales data from a CSV file and appends it to the sales_data list.
    The function also validates the filename and ensures that the file has not already been imported.
    
    :param sales_data: The list that will be appended with sales data.
    :param file_path: The path to the CSV file to be imported.
    :return: True if the import was successful, False if any error occurred.
    """
    file_name = file_path.name
    
    # Validate the filename format
    if not is_valid_filename_format(file_name):
        print(f"Error: Filename '{file_name}' doesn't follow the expected format of 'sales_qn_yyyy_r.csv'.")
        return False  # Exit the function if the filename is invalid
    
    # Check if the file has already been imported
    if already_imported(file_path):
        print(f"Error: File '{file_name}' has already been imported.")
        return False  # Exit the function if the file has already been imported
    
    # Check if the file exists
    if not file_path.is_file():
        print(f"Error: Sales file '{file_name}' not found.")
        return False  # Exit the function if the file doesn't exist
    
    try:
        # Try to read and import sales data from the file
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if len(line) > 0:  # Skip empty lines
                    *amount_sales_date, region_code = line
                    # Append the sales data to the sales_data list
                    sales_data.append({
                        "amount": float(amount_sales_date[0]),  # Convert amount to float
                        "sales_date": amount_sales_date[1],     # Use sales date directly
                        "region": region_code                    # Region code
                    })
        # Mark the file as imported
        add_imported_file(file_path)  # Assuming this function adds to an 'imported' list
        print(f"Successfully imported sales data from '{file_name}'.")
        return True  # Indicate successful import
    except FileNotFoundError:
        print(f"Error: Sales file '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred while importing the file '{file_name}': {e}")
    
    return False  # Return False if there was any error


# Main menu function
def main_menu():
    sales_data = []  # Initialize the sales data list
    while True:
        print("\nCOMMAND MENU")
        print("view - View all sales")
        print("add1 - Add sales by typing sales, year, month, day, and region")
        print("add2 - Add sales by typing sales, date (YYYY-MM-DD), and region")
        print("import - Import sales from file")
        print("menu - Show menu")
        print("exit - Exit program")

        command = input("Please enter a command: ").lower()

        # Perform actions based on the user's command
        if command == 'view':
            view_sales(sales_data)
        elif command == 'add1':
            add_sale_by_components(sales_data)
        elif command == 'add2':
            add_sale_by_date(sales_data)
        elif command == 'import':
            import_all_sales(sales_data)
        elif command == 'menu':
            continue  # Just loops back to the menu
        elif command == 'exit':
            print("Saved sales records. Bye!")
            break  # Exits the loop and ends the program
        else:
            print("Invalid command. Please try again.")

# Start the program by calling the main_menu function
if __name__ == "__main__":
    main_menu()
