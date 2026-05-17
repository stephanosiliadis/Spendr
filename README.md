# SPENDR CLI

**Spendr CLI** is a lightweight command-line application for tracking personal finances.
It allows you to **record income and expenses, retrieve past transactions, edit or delete entries, and analyze financial insights** directly from the terminal.

The application is written in **Python** and uses:

* **SQLite** for persistent storage
* **Typer** for modern CLI commands
* **Rich** for clean, color-coded terminal tables

Spendr can be used **interactively through a menu** or **through direct CLI commands**, making it suitable for both casual users and power users.

---

# Features

* Add new **Income** or **Expense** transactions
* Retrieve stored transactions
* Edit transactions by ID
* Delete transactions by ID
* Display **financial insights**
* Interactive CLI menu
* Direct command usage with flags
* Flexible date parsing (`today`, `yesterday`, `YYYY-MM-DD`)
* Clean terminal tables using **Rich**
* Standalone executable support (`Spendr.exe`)

---

# Project Structure

```
Spendr/
│
├── main.py                 # Typer CLI entry point
│
├── data/
│   └── transactions.db     # SQLite database
│
├── models/
│   └── Transaction.py      # Transaction dataclass
│
├── utils/
│   ├── db.py               # Database functions
│   ├── handlers.py         # Transaction handlers
│   ├── io.py               # CLI input/output helpers
│   ├── retrieveactions.py  # Retrieval action mapping
│   └── parsetransactiondate.py # Flexible date parsing
│
├── dist/
│   └── Spendr.exe          # Packaged executable (PyInstaller)
│
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/stephanosiliadis/Spendr.git
cd Spendr
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

---

# Usage

Spendr can be used in **two different modes**.

---

# 1. Interactive Menu Mode

If you run the program **without a command**, the interactive menu starts.

```
python main.py
```

Example:

```
=== SPENDR CLI ===

Available Actions:
1. Insert new transaction
2. Retrieve past transactions
3. Delete single transaction
4. Edit single transaction
5. Get transaction insights
6. End Session
```

This mode is ideal for casual users.

---

# 2. Command Mode (Typer CLI)

Spendr also supports direct CLI commands.

```
python main.py COMMAND [OPTIONS]
```

or if using the executable:

```
Spendr.exe COMMAND [OPTIONS]
```

---

# Add a Transaction

```
python main.py add
```

You will be prompted interactively.

You can also provide parameters directly:

```
python main.py add --type Income --amount 100 --description "Salary" --date today
```

Short flags are supported:

```
python main.py add -t Expense -a 50 -d "Groceries" -D yesterday
```

Supported date formats:

* `today`
* `yesterday`
* `YYYY-MM-DD`

---

# List Transactions

Display all stored transactions.

```
python main.py list
```

Example output:

```
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID ┃ Type     ┃ Amount   ┃ Description       ┃ Date       ┃
┣━━━━╋━━━━━━━━━━╋━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━┫
┃ 1  ┃ Income   ┃ +100.00€ ┃ Salary            ┃ 2026-03-11 ┃
┃ 2  ┃ Expense  ┃ -79.16€  ┃ JUMBO Groceries   ┃ 2026-03-10 ┃
┗━━━━┻━━━━━━━━━━┻━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━┛
```

Income values appear **green** and expenses appear **red**.

---

# Delete a Transaction

Delete a transaction by ID.

```
python main.py delete --id 3
```

Example confirmation:

```
You will delete the following transaction:
(ID, Type, Amount, Description, Date)

Proceed with deletion? (y/n)
```

---

# Edit a Transaction

Edit a transaction by ID. Spendr displays the matching transaction first and asks for confirmation before prompting for new values.

```
python main.py edit --id 3
```

Press ENTER for any field you want to keep unchanged.

---

# View Insights

Display financial statistics calculated from your transactions.

```
python main.py insights
```

Example:

```
Transaction Insights

Total Income:        +100.00€
Total Expenses:      -81.66€
Net Balance:          18.34€
Highest Income:      +100.00€ (Salary)
Highest Expense:     -79.16€ (Groceries)
Average Transaction:  60.55€
```

---

# Creating a Standalone Executable

Spendr can be packaged into a standalone executable using **PyInstaller**.

Install PyInstaller:

```
pip install pyinstaller
```

Build the executable:

```
pyinstaller --onefile --name Spendr main.py
```

The executable will appear in:

```
dist/Spendr.exe
```

You can distribute this file and it will work **without requiring Python or any packages**.

---

# Example Executable Usage

```
Spendr.exe
Spendr.exe add -t Income -a 1200 -d "Salary" -D today
Spendr.exe list
Spendr.exe edit --id 5
Spendr.exe delete --id 5
Spendr.exe insights
```

---

# Future Improvements

Possible enhancements for Spendr:

* Export transactions to CSV or JSON
* Monthly spending reports
* Budget tracking
* Graphs in terminal
* Mobile interface
* Automatic recurring transactions

---

# License

This project is licensed under the MIT License.
