import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Initialize expenses list
        self.expenses = []
        
        # Categories for dropdown
        self.categories = [
            "Food", "Transport", "Shopping", 
            "Entertainment", "Bills", "Healthcare", 
            "Education", "Other"
        ]
        
        # Create GUI
        self.setup_gui()
        
        # Load data if available
        self.load_data()
    
    def setup_gui(self):
        # Styling
        self.bg_color = "#f5f5f5"
        self.button_color = "#4a7a8c"
        self.text_color = "#333333"
        
        self.root.config(bg=self.bg_color)
        
        # Header
        self.header = tk.Label(
            self.root,
            text="Expense Tracker",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.header.pack(pady=10)
        
        # Input Frame
        self.input_frame = tk.Frame(self.root, bg=self.bg_color)
        self.input_frame.pack(pady=10)
        
        # Amount
        tk.Label(
            self.input_frame,
            text="Amount (₹):",
            bg=self.bg_color,
            font=("Helvetica", 10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.amount_entry = tk.Entry(
            self.input_frame,
            width=15,
            font=("Helvetica", 10)
        )
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Category
        tk.Label(
            self.input_frame,
            text="Category:",
            bg=self.bg_color,
            font=("Helvetica", 10)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            self.input_frame,
            textvariable=self.category_var,
            values=self.categories,
            width=15,
            font=("Helvetica", 10)
        )
        self.category_dropdown.grid(row=0, column=3, padx=5, pady=5)
        self.category_dropdown.set("Food")  # Default
        
        # Description
        tk.Label(
            self.input_frame,
            text="Description:",
            bg=self.bg_color,
            font=("Helvetica", 10)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.desc_entry = tk.Entry(
            self.input_frame,
            width=40,
            font=("Helvetica", 10)
        )
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Date
        tk.Label(
            self.input_frame,
            text="Date:",
            bg=self.bg_color,
            font=("Helvetica", 10)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.date_entry = tk.Entry(
            self.input_frame,
            width=15,
            font=("Helvetica", 10)
        )
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today
        
        # Add Expense Button
        self.add_button = tk.Button(
            self.input_frame,
            text="Add Expense",
            command=self.add_expense,
            bg=self.button_color,
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10
        )
        self.add_button.grid(row=2, column=3, padx=5, pady=5)
        
        # Expense List (Treeview)
        self.tree_frame = tk.Frame(self.root, bg=self.bg_color)
        self.tree_frame.pack(pady=10)
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Amount", "Category", "Description", "Date"),
            show="headings",
            height=15
        )
        
        # Define columns
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Amount", text="Amount (₹)", anchor="center")
        self.tree.heading("Category", text="Category", anchor="center")
        self.tree.heading("Description", text="Description", anchor="center")
        self.tree.heading("Date", text="Date", anchor="center")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Amount", width=100, anchor="center")
        self.tree.column("Category", width=120, anchor="center")
        self.tree.column("Description", width=250, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        
        self.tree.pack(side="left")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Summary Frame
        self.summary_frame = tk.Frame(self.root, bg=self.bg_color)
        self.summary_frame.pack(pady=10)
        
        self.total_label = tk.Label(
            self.summary_frame,
            text="Total Spent: $0.00",
            bg=self.bg_color,
            font=("Helvetica", 12, "bold")
        )
        self.total_label.pack(side="left", padx=10)
        
        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        self.buttons_frame.pack(pady=10)
        
        # Delete Button
        self.delete_button = tk.Button(
            self.buttons_frame,
            text="Delete Selected",
            command=self.delete_expense,
            bg="#8c4a4a",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10
        )
        self.delete_button.pack(side="left", padx=5)
        
        # Save Button
        self.save_button = tk.Button(
            self.buttons_frame,
            text="Save Data",
            command=self.save_data,
            bg="#4a8c5e",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10
        )
        self.save_button.pack(side="left", padx=5)
        
        # Filter Button
        self.filter_button = tk.Button(
            self.buttons_frame,
            text="Filter by Category",
            command=self.filter_by_category,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10
        )
        self.filter_button.pack(side="left", padx=5)
        
        # Update the display
        self.update_display()
    
    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_var.get()
        description = self.desc_entry.get()
        date = self.date_entry.get()
        
        if not amount or not category:
            messagebox.showerror("Error", "Amount and Category are required!")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive number!")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format!")
            return
        
        expense = {
            "id": len(self.expenses) + 1,
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }
        
        self.expenses.append(expense)
        self.update_display()
        
        # Clear inputs
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
    
    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No expense selected!")
            return
        
        item_id = int(self.tree.item(selected_item)["values"][0])
        self.expenses = [exp for exp in self.expenses if exp["id"] != item_id]
        self.update_display()
    
    def filter_by_category(self):
        category = self.category_var.get()
        filtered_expenses = [exp for exp in self.expenses if exp["category"] == category]
        
        self.tree.delete(*self.tree.get_children())
        for exp in filtered_expenses:
            self.tree.insert("", "end", values=(
                exp["id"],
                f"${exp['amount']:.2f}",
                exp["category"],
                exp["description"],
                exp["date"]
            ))
        
        total = sum(exp["amount"] for exp in filtered_expenses)
        self.total_label.config(text=f"Total Spent (Filtered): ₹{total:.2f}")
    
    def update_display(self):
        self.tree.delete(*self.tree.get_children())
        for exp in self.expenses:
            self.tree.insert("", "end", values=(
                exp["id"],
                f"${exp['amount']:.2f}",
                exp["category"],
                exp["description"],
                exp["date"]
            ))
        
        total = sum(exp["amount"] for exp in self.expenses)
        self.total_label.config(text=f"Total Spent: ₹{total:.2f}")
    
    def save_data(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Expense Data"
        )
        
        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(self.expenses, f)
                messagebox.showinfo("Success", "Data saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Load Expense Data"
        )
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    self.expenses = json.load(f)
                self.update_display()
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
