# Standard Library Imports
from decimal import Decimal, ROUND_HALF_UP  # For precise currency and numeric operations
import locale as lc  # For formatting currency and regional data
from p01sc06_OOPDBGUI3tier.p01beg_1da_sales import DataFileAccess, ImportedFile, InputAccess, Regions, Sales, SalesFile, SalesList # Project-specific imports for DataFileAccess, SalesList, etc.

# Set locale for currency formatting
lc.setlocale(lc.LC_ALL, "en_US")

# SalesManager Class
class SalesManager:
    def __init__(self, sales_list=None):
        # Initialize the DataFileAccess object
        self._datafileaccess = DataFileAccess()

    @staticmethod
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

    def add_sales1(self) -> None:
        """Add a sale by entering individual components."""
        kwarg = InputAccess.from_input1()
        sales = Sales(**kwarg)
        self._datafileaccess.add_sales(sales)
        print(f"Sales for {kwarg['sales_date']} is added.\n")
        print(f"add_sales1: {DataFileAccess.SALES_ID['Sales']=}")

    def add_sales2(self) -> None:
        """Add a sale by entering the full date."""
        kwarg = InputAccess.from_input2()
        sales = Sales(**kwarg)
        self._datafileaccess.add_sales(sales)
        print(f"Sales for {kwarg['sales_date']} is added.\n")
        print(f"add_sales2: {DataFileAccess.SALES_ID['Sales']=}")

    def import_sales(self) -> None:
        """Import sales data from a file."""
        filename = input("Enter name of file to import: ")
        salesfile = SalesFile(filename)
        importedfile = ImportedFile()

        # Validate filename format and region code
        if not salesfile.is_valid_filename_format:
            print(f"Filename '{filename}' doesn't follow the expected",
                  f"format of '{salesfile.NAMING_CONVENTION}'.")
        elif Regions().get(salesfile.get_region_code()) is None:
            print(f"Filename '{filename}' doesn't include one of",
                  f"the following region codes: {[region.code for region in Regions()]}.")
        elif importedfile.already_imported(salesfile._sales_filepath_name):
            filename = filename.replace("\n", "")  
            print(f"File '{filename}' has already been imported.")
        else:
            # Attempt to import the file
            try:
                imported_sales_list = salesfile.import_sales()
            except Exception as e:  
                print(f"{type(e)}. Fail to import sales from '{filename}'.")
            else:
                has_bad_data = self.view_sales(imported_sales_list)
                if has_bad_data:
                    print(f"File '{filename}' contains bad data.\n"
                         "Please correct the data in the file and try again.")
                elif imported_sales_list.count > 0:  
                    self._datafileaccess.concat_saleslist(imported_sales_list)    
                    print("Imported sales added to list.")
                    importedfile.add_imported_file(salesfile._sales_filepath_name)


# Main Function
def main():
    # Initialize the SalesManager
    salesmanager = SalesManager()

    # View all sales
    salesmanager.view_sales(salesmanager._datafileaccess._all_sales_list)
    print(f"{salesmanager._datafileaccess.SALES_ID['Sales']=}")

    # Import sales from a file
    salesmanager.import_sales()

    # View updated sales
    salesmanager.view_sales(salesmanager._datafileaccess._all_sales_list)
    print(f"{salesmanager._datafileaccess.SALES_ID['Sales']=}")

    # Save all sales to the file
    salesmanager._datafileaccess.save_all_sales()


# Entry Point
if __name__ == '__main__':
    main()
