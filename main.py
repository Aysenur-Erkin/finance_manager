import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

from data_manager import DatabaseManager
from classifier import ExpenseClassifier
from reporter import Reporter

DEFAULT_CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Health", "Entertainment", "Other"]
MIN_TRAIN_ROWS = 5


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

    def _categories(self):
        # defaults first, then whatever the user typed before
        result = list(DEFAULT_CATEGORIES)
        for cat in self.db.get_categories():
            if cat != 'Unknown' and cat.lower() not in (c.lower() for c in result):
                result.append(cat)
        return result

    def _ask_category(self, title, description, current=None, hint=""):
        win = tk.Toplevel(self)
        win.title(title)
        win.resizable(False, False)
        win.transient(self)

        frame = ttk.Frame(win, padding=15)
        frame.pack(fill='both')
        ttk.Label(frame, text=description, font=('Helvetica', 11, 'bold'), wraplength=280).pack(anchor='w')
        if hint:
            ttk.Label(frame, text=hint, foreground='gray').pack(anchor='w', pady=(2, 0))

        choice = tk.StringVar(value=current or "")
        box = ttk.Combobox(frame, textvariable=choice, values=self._categories(), width=30)
        box.pack(fill='x', pady=(10, 10))
        box.focus_set()

        result = {'category': None}

        def ok(event=None):
            text = choice.get().strip()
            if not text:
                box.focus_set()
                return
            # "food" and "Food" should not become two different classes
            for cat in self._categories():
                if cat.lower() == text.lower():
                    text = cat
                    break
            result['category'] = text
            win.destroy()

        buttons = ttk.Frame(frame)
        buttons.pack(fill='x')
        ttk.Button(buttons, text="Cancel", command=win.destroy).pack(side='right')
        ttk.Button(buttons, text="OK", command=ok).pack(side='right', padx=(0, 5))
        win.bind('<Return>', ok)
        win.bind('<Escape>', lambda event: win.destroy())

        win.grab_set()
        self.wait_window(win)
        return result['category']

    def _add_expense(self):
        amount = simpledialog.askfloat("Amount", "Enter expense amount:", parent=self)
        if amount is None:
            return
        description = simpledialog.askstring("Description", "Enter description:", parent=self)
        if not description:
            return

        guess = self.classifier.predict_category(description)
        if guess:
            hint = f"Model suggests: {guess} (change it if it's wrong)"
        else:
            hint = "No trained model yet, pick a category"
        category = self._ask_category("Category", description, current=guess, hint=hint)
        if not category:
            return

        self.db.add_expense(amount, description, category)
        messagebox.showinfo("Success", f"Expense added:\n{amount} - {description} ({category})")

    def _list_expenses(self):
        win = tk.Toplevel(self)
        win.title("Expenses")
        win.geometry("650x400")

        top = ttk.Frame(win, padding=(10, 10, 10, 5))
        top.pack(fill='x')
        ttk.Label(top, text="Category:").pack(side='left')
        selected = tk.StringVar(value="All")
        filter_box = ttk.Combobox(top, textvariable=selected, state='readonly', width=18)
        filter_box.pack(side='left', padx=5)
        ttk.Label(top, text="double-click a row to change its category", foreground='gray').pack(side='right')

        table_frame = ttk.Frame(win, padding=(10, 0, 10, 10))
        table_frame.pack(fill='both', expand=True)
        columns = ('date', 'amount', 'description', 'category')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        tree.heading('date', text="Date")
        tree.heading('amount', text="Amount")
        tree.heading('description', text="Description")
        tree.heading('category', text="Category")
        tree.column('date', width=140, stretch=False)
        tree.column('amount', width=80, anchor='e', stretch=False)
        tree.column('description', width=240)
        tree.column('category', width=110, stretch=False)
        scroll = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

        def fill():
            filter_box['values'] = ["All"] + self.db.get_categories()
            category = None if selected.get() == "All" else selected.get()
            tree.delete(*tree.get_children())
            for e in self.db.get_expenses(category=category):
                tree.insert('', 'end', iid=str(e['id']),
                            values=(e['date'], f"{e['amount']:.2f}", e['description'], e['category']))

        def edit(event):
            row = tree.identify_row(event.y)
            if not row:
                return
            date, amount, description, old = tree.item(row, 'values')
            new = self._ask_category("Change category", description,
                                     current=None if old == 'Unknown' else old,
                                     hint=f"{date}  |  {amount}  |  now: {old}")
            if new and new != old:
                self.db.update_category(int(row), new)
                fill()

        filter_box.bind('<<ComboboxSelected>>', lambda event: fill())
        tree.bind('<Double-1>', edit)
        fill()

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
        expenses = self.db.get_labeled_expenses()
        categories = {e['category'] for e in expenses}
        if len(expenses) < MIN_TRAIN_ROWS or len(categories) < 2:
            messagebox.showwarning(
                "Warning",
                f"Need at least {MIN_TRAIN_ROWS} expenses in 2 different categories to train.\n"
                f"Now: {len(expenses)} expenses, {len(categories)} categories."
            )
            return
        self.classifier.train(expenses)
        self.classifier.save_model()
        messagebox.showinfo("Success", f"Classifier trained on {len(expenses)} expenses ({len(categories)} categories).")


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
