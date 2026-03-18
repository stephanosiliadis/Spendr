# Import standard library packages.
import os
import sqlite3
from datetime import date

# Import third library packages.
import pandas as pd

# Import local packages.
from models.Transaction import Transaction

# Paths.
DATA_DIR = "data"
DB_NAME = "transactions.db"

# Make the data directory if it does not exist.
os.makedirs(DATA_DIR, exist_ok=True)


def create_db_tables() -> None:
    """
    Create the SQLite database and a table to store transactions.

    The table `transactions` includes the following columns:
        - id: INTEGER PRIMARY KEY AUTOINCREMENT
        - type: TEXT (Income or Expense)
        - amount: FLOAT
        - description: TEXT
        - date: DATE

    Returns:
        None
    """
    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Create the table.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type TEXT NOT NULL,
                            amount FLOAT NOT NULL,
                            description TEXT NOT NULL,
                            date DATE NOT NULL
            )
            """
        )

        # Commit the changes to the database.
        conn.commit()


def insert_transaction(transaction: Transaction) -> None:
    """
    Insert a Transaction into the database.

    Args:
        transaction (Transaction): A Transaction object containing:
            - type (str): "Income" or "Expense"
            - amount (float)
            - description (str)
            - date (datetime.date or datetime.datetime)

    Returns:
        None
    """
    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        cursor.execute(
            "INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)",
            (
                transaction.type,
                transaction.amount,
                transaction.description,
                transaction.date.isoformat(),
            ),
        )

        # Commit the changes to the database.
        conn.commit()


def retrieve_transactions():
    """
    Retrieve all transactions from the database.

    Returns:
        Sequence[TransactionRow]: Sequence of all transactions as tuples:
            (id, type, amount, description, date)
    """
    transactions = []

    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        query = cursor.execute("SELECT * FROM transactions")
        transactions = query.fetchall()

        # Commit the changes to the database.
        conn.commit()

    return transactions


def retrieve_transactions_by_date(start_date: date, end_date: date):
    """
    Retrieve transactions that occurred within a specific date range.

    Args:
        start_date (date): The start date (inclusive)
        end_date (date): The end date (inclusive)

    Returns:
        Sequence[TransactionRow]: Transactions between start_date and end_date
    """
    transactions = []

    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        query = cursor.execute(
            "SELECT * FROM transactions WHERE date BETWEEN ? AND ? ORDER BY date",
            (start_date, end_date),
        )
        transactions = query.fetchall()

        # Commit the changes to the database.
        conn.commit()

    return transactions


def retrieve_transactions_by_amount(min_amount: float, max_amount: float):
    """
    Retrieve transactions within a specified amount range.

    Args:
        min_amount (float): Minimum transaction amount (inclusive)
        max_amount (float): Maximum transaction amount (inclusive)

    Returns:
        Sequence[TransactionRow]: Transactions where amount is between min_amount and max_amount
    """
    transactions = []

    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        query = cursor.execute(
            "SELECT * FROM transactions WHERE amount BETWEEN ? AND ? ORDER BY date",
            (min_amount, max_amount),
        )
        transactions = query.fetchall()

        # Commit the changes to the database.
        conn.commit()

    return transactions


def retrieve_transactions_by_type(type: str):
    """
    Retrieve transactions filtered by type ("Income" or "Expense").

    Args:
        type (str): Type of transaction to retrieve ("Income" or "Expense")

    Returns:
        Sequence[TransactionRow]: Transactions matching the specified type
    """
    transactions = []

    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        query = cursor.execute(
            "SELECT * FROM transactions WHERE type=?  ORDER BY date",
            (type,),
        )
        transactions = query.fetchall()

        # Commit the changes to the database.
        conn.commit()

    return transactions


def retrieve_transaction(transaction_id: int):
    """
    Retrieve a single transaction by its ID.

    Args:
        transaction_id (int): The ID of the transaction to retrieve

    Returns:
        Sequence[TransactionRow]: A Sequence with the transaction as a tuple, or an empty Sequence if not found
    """
    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        query = cursor.execute(
            "SELECT * FROM transactions WHERE id=?",
            (transaction_id,),
        )
        transaction = query.fetchall()

        # Commit the changes to the database.
        conn.commit()

    return transaction


def delete_transaction(transaction_id: int) -> None:
    """
    Delete a transaction from the database by its ID.

    Args:
        transaction_id (int): The ID of the transaction to delete

    Returns:
        None
    """
    # Create the db connection and cursor instance.
    with sqlite3.connect(os.path.join(DATA_DIR, DB_NAME)) as conn:
        cursor = conn.cursor()

        # Perform the Query.
        cursor.execute(
            "DELETE FROM transactions WHERE id=?",
            (transaction_id,),
        )

        # Commit the changes to the database.
        conn.commit()


def save_transactions(transactions, format, title):
    df = pd.DataFrame(
        transactions, columns=["ID", "Type", "Amount", "Description", "Date"]
    )
    if format == "Excel":
        with pd.ExcelWriter(f"data/{title}.xlsx") as writer:
            df.to_excel(writer, index=False)
    elif format == "CSV":
        df.to_csv(f"data/{title}.csv", index=False)
    elif format == "JSON":
        df.to_json(f"data/{title}.json", orient="records", date_format="iso")
    elif format == "Database File":
        conn = sqlite3.connect(f"data/{title}.db")
        df.to_sql("transactions", conn, if_exists="replace", index=False)
        conn.close()
