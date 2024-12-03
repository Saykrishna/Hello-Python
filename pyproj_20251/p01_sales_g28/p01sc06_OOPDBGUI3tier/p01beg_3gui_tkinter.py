import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
import p01sc06_OOPDBGUI3tier.p01beg_1db_sales_db as db
from p01sc06_OOPDBGUI3tier.p01beg_1da_sales import Sales, Regions

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SalesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10 10 10 10")
        self.parent = parent

        # String variables for input fields
        self.salesDate = tk.StringVar()
        self.region = tk.StringVar()
        self.amount = tk.StringVar()
        self.id = tk.StringVar()

        # Database access
        self.sqlite_dbaccess = db.SQLiteDBAccess()
        self.sales = None

        self.init_components()

    def init_components(self):
        self.pack()

        # Labels and Entry Widgets
        ttk.Label(self, text="Enter date and region to get sales amount").grid(row=0, column=0, columnspan=4)

        ttk.Label(self, text="Date:").grid(row=1, column=0, sticky=tk.E)
        self.salesDate_entry = ttk.Entry(self, width=25, textvariable=self.salesDate)  # Store the reference
        self.salesDate_entry.grid(row=1, column=1, columnspan=2)

        ttk.Label(self, text="Region:").grid(row=2, column=0, sticky=tk.E)
        self.region_entry = ttk.Entry(self, width=25, textvariable=self.region)  # Store the reference
        self.region_entry.grid(row=2, column=1, columnspan=2)

        ttk.Label(self, text="Amount:").grid(row=3, column=0, sticky=tk.E)
        self.amount_entry = ttk.Entry(self, width=25, textvariable=self.amount, state=tk.DISABLED)  # Store the reference
        self.amount_entry.grid(row=3, column=1, columnspan=2)

        ttk.Label(self, text="ID:").grid(row=4, column=0, sticky=tk.E)
        self.id_entry = ttk.Entry(self, width=25, textvariable=self.id, state="readonly")  # Store the reference
        self.id_entry.grid(row=4, column=1, columnspan=2)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=4, sticky=tk.E)

        ttk.Button(button_frame, text="Get Amount", command=self.get_amount).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear Field", command=self.clear_field).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Save Changes", command=self.save_changes, state=tk.DISABLED).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.parent.destroy).grid(row=0, column=3, padx=5)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


    def get_amount(self):
        sales_date = self.salesDate.get().strip()
        region_code = self.region.get().strip()

        if not sales_date or not region_code:
            messagebox.showerror("Error", "Please enter both date and region.")
            return

        try:
            sales_date = datetime.strptime(sales_date, Sales.DATE_FORMAT).date()
        except ValueError:
            messagebox.showerror("Error", f"{sales_date} is not in a valid date format ('yyyy-mm-dd').")
            return

        try:
            regions = self.sqlite_dbaccess.retrieve_regions()
            region_codes = [region.code for region in regions]

            if region_code not in region_codes:
                messagebox.showerror("Error", f"{region_code} is not a valid region code. Valid codes: {region_codes}")
                return

            self.sales = self.sqlite_dbaccess.retrieve_sales_by_date_region(sales_date, region_code)

            if not self.sales:
                self.amount.set("")
                self.id.set("")
                messagebox.showerror("Error", "No sales record found for the specified date and region.")
            else:
                self.amount.set(self.sales.amount)
                self.id.set(self.sales.id)
                self.enable_editing()
        except Exception as e:
            logging.error(f"Database error during get_amount: {e}")
            messagebox.showerror("Database Error", "An error occurred while retrieving sales data.")

    def clear_field(self):
        self.salesDate.set("")
        self.region.set("")
        self.amount.set("")
        self.id.set("")
        self.disable_editing()

    def save_changes(self):
        if not self.id.get():
            messagebox.showerror("Error", "No sales record to save.")
            return

        try:
            new_amount = float(self.amount.get())
            self.sales.amount = new_amount
            self.sqlite_dbaccess.update_sales(self.sales)
            messagebox.showinfo("Success", "Sales record updated successfully.")
            self.clear_field()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")
        except Exception as e:
            logging.error(f"Database error during save_changes: {e}")
            messagebox.showerror("Database Error", "An error occurred while saving the changes.")

    def enable_editing(self):
        for widget in [self.salesDate_entry, self.region_entry]:
            widget.config(state=tk.DISABLED)
        self.amount_entry.config(state=tk.NORMAL)
        self.saveChanges_button.config(state=tk.NORMAL)

    def disable_editing(self):
        for widget in [self.salesDate_entry, self.region_entry]:
            widget.config(state=tk.NORMAL)
        self.amount_entry.config(state=tk.DISABLED)
        self.saveChanges_button.config(state=tk.DISABLED)


def main():
    try:
        root = tk.Tk()
        root.title("Edit Sales Amount")
        SalesFrame(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Error", "An unexpected error occurred.")


if __name__ == "__main__":
    main()