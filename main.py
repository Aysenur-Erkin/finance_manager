import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

from data_manager import DatabaseManager
from classifier import ExpenseClassifier
from reporter import Reporter

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Finance Manager")
        self.geometry("450x450")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'))
        style.configure('TButton', font=('Helvetica', 12), padding=8)
        style.map('TButton', background=[('active', '#77b0e6')])

        self.db = DatabaseManager(db_path="expenses.db")
        self.classifier = ExpenseClassifier()
        self.reporter = Reporter(self.db)

        header = ttk.Label(self, text="Smart Finance Manager", style='Header.TLabel')
        header.pack(pady=(0, 15))

        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', expand=True)

        actions = [
            ("Add Expense", self._add_expense),
            ("List Expenses", self._list_expenses),
            ("Create Report", self._create_report),
            ("Train Classifier", self._train_model),
            ("Exit", self.quit)
        ]
        for idx, (label, command) in enumerate(actions):
            button = ttk.Button(button_frame, text=label, command=command)
            button.grid(row=idx, column=0, sticky='ew', pady=5)
        button_frame.columnconfigure(0, weight=1)

    def _add_expense(self):
        amount = simpledialog.askfloat("Amount", "Enter expense amount:", parent=self)
        if amount is None:
            return
        description = simpledialog.askstring("Description", "Enter description:", parent=self)
        if not description:
            return
        category = self.classifier.predict_category(description)
        self.db.add_expense(amount, description, category)
        messagebox.showinfo("Success", f"Expense added:\n{amount} - {description} ({category})")

    def _list_expenses(self):
        category = simpledialog.askstring("Category", "Category:", parent=self) or None
        limit = simpledialog.askinteger("Limit", "Number of records to show:", parent=self)
        expenses = self.db.get_expenses(category=category, limit=limit)
        if not expenses:
            messagebox.showinfo("Expenses", "No expenses found.")
            return
        expense_text = "\n".join(
            f"{e['date']} | {e['amount']} | {e['description']} | {e['category']}" for e in expenses
        )
        messagebox.showinfo("Expenses", expense_text)

    def _create_report(self):
        period = simpledialog.askstring("Period", "Enter period (daily/monthly):", parent=self)
        if period not in ['daily', 'monthly']:
            messagebox.showerror("Error", "Invalid period. Must be 'daily' or 'monthly'.")
            return
        summary = self.db.get_summary(period=period)
        report_text = self.reporter.format_summary(summary)
        chart_text = self.reporter.ascii_chart(summary)
        messagebox.showinfo("Report", report_text + "\n\n" + chart_text)

    def _train_model(self):
        expenses = self.db.get_expenses()
        if not expenses:
            messagebox.showwarning("Warning", "Not enough data to train the classifier.")
            return
        self.classifier.train(expenses)
        self.classifier.save_model()
        messagebox.showinfo("Success", "Classifier trained and saved successfully.")

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
