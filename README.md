# Smart Personal Finance Manager

A lightweight Python application to track personal expenses, featuring a simple graphical user interface (GUI) built with Tkinter and backend components for data management and machine learning–powered category prediction. 🐍💼

---

## Features ✨

* **Add Expense** ➕: Enter amount and description, category is automatically predicted by a trained model.
* **List Expenses** 📋: View all expenses, filtered by category or limited in number.
* **Create Report** 📊: Generate daily or monthly summaries with ASCII bar charts.
* **Train Classifier** 🤖: Retrain the machine learning model on existing data.
* **GUI-Only** 🖥️: No command-line interaction required—just run in PyCharm.

---

## Tech Stack 🔧

* **Python**
* **SQLite** for local data storage
* **scikit-learn** (RandomForest + TF-IDF) for category prediction
* **tabulate** for formatted tables
* **Tkinter / ttk** for GUI

---

## Directory Structure

```plaintext
finance_manager/
├── main.py               # GUI entry point (Tkinter application)
├── data_manager.py       # SQLite database manager
├── classifier.py         # ML-based expense classifier
├── reporter.py           # Summary formatter and ASCII chart generator
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## Prerequisites

* Python
* (Optional) Virtual environment tool (venv or virtualenv)

---

## Installation 🛠️

1. **Clone the repository**

   ```bash
   git clone https://github.com/Aysenur-Erkin/finance_manager.git
   cd finance_manager
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   # Windows (PowerShell):
   venv\Scripts\Activate.ps1
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application ▶️

Open the project in PyCharm and simply **Run** the `main.py` script:

1. In the **Project** pane, right‑click on `main.py`.
2. Select **Run 'main'**.
3. The GUI window will launch.

---

## Using the GUI 🖥️

When the application window opens, you will see five buttons styled in a clean interface:

* **Add Expense**

  1. A dialog labeled **Amount** will appear. Enter a numeric value (e.g., `12.50`) and click \*\*OK\`.
  2. Next, a **Description** dialog will appear. Enter text (e.g., `Lunch at cafe`) and click \*\*OK\`.
  3. A confirmation message shows the saved expense.

* **List Expenses**

  1. A **Category** dialog appears. Type a category to filter (e.g., `Food`) or leave blank to view all and click \*\*OK\`.
  2. Then, a **Limit** dialog appears. Enter a number (e.g., `10`) or leave blank to list all and click \*\*OK\`.
  3. An information window displays the matching expense records.

* **Create Report**

  1. A **Period** dialog prompts for `daily` or `monthly`. Type one of these and click \*\*OK\`.
  2. A report window shows a formatted table and ASCII bar chart summarizing expenses.

* **Train Classifier**
  Retrains the underlying machine learning model on all stored expense data. A popup will confirm once training and saving are complete.

* **Exit**
  Closes the application immediately.

---

## Testing 🧪

Since we run everything in PyCharm, simply run the `main.py` script in PyCharm to test the application. 🖥️🚀

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

*Happy budgeting!* 🎉
