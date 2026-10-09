# Finance manager

Small Tkinter app for logging expenses. Amount and description go into SQLite. The category comes from a scikit-learn model (TF-IDF plus a random forest) if it has been trained. Reports are a table and an ASCII bar chart, daily or monthly.

## Run

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

On macOS or Linux, `source venv/bin/activate`. PyCharm'da `main.py` uzerine sag tiklayip Run da ayni isi yapar.

## Buttons

Add Expense asks for amount, then description, then saves the row. List Expenses can filter by category and limit the rows. Create Report asks for `daily` or `monthly`. Train Classifier fits the model on the rows already in the database and saves it. Exit closes the window.

There is no test suite. `python main.py` is how I check it.

## Files

```
main.py           window
data_manager.py   sqlite
classifier.py     category model
reporter.py       table and chart
```

MIT. See LICENSE.
