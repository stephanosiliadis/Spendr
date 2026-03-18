# Import local packages.
from utils.io import *
from utils.db import (
    retrieve_transactions,
    retrieve_transactions_by_type,
    retrieve_transactions_by_amount,
    retrieve_transactions_by_date,
)


def action_all_transactions():
    """
    Retrieve all transactions from the database.

    Returns:
        Tuple[Sequence[TransactionRow], str]:
            - transactions (Sequence[TransactionRow]): Sequence of all transaction tuples
            - title (str): Table title string
    """
    transactions = retrieve_transactions()
    title = "All Transactions"
    return transactions, title


def action_by_date_range():
    """
    Retrieve transactions within a specified date range.
    Prompts the user for start and end dates.

    Returns:
        Tuple[Sequence[TransactionRow], str]:
            - transactions (Sequence[TransactionRow]): Sequence of transactions within the date range
            - title (str): Table title string describing the range
    """
    start_date = input_transaction_date("Enter the start date (YYYY-MM-DD): ")
    end_date = input_transaction_date(
        "Enter the end date (YYYY-MM-DD or press 'Enter' for today): "
    )
    transactions = retrieve_transactions_by_date(start_date, end_date)
    title = f"Transactions from {start_date} to {end_date}"
    return transactions, title


def action_by_amount_range():
    """
    Retrieve transactions within a specified amount range.
    Prompts the user for minimum and maximum amounts.

    Returns:
        Tuple[Sequence[TransactionRow], str]:
            - transactions (Sequence[TransactionRow]): Sequence of transactions within the amount range
            - title (str): Table title string describing the range
    """
    min_amount = input_transaction_amount("Enter the minimum amount: ")
    max_amount = input_transaction_amount("Enter the maximum amount: ")
    transactions = retrieve_transactions_by_amount(min_amount, max_amount)
    title = f"Transactions between €{min_amount} and €{max_amount}"
    return transactions, title


def action_by_type():
    """
    Retrieve transactions of a specific type (Income or Expense).
    Prompts the user to select the type.

    Returns:
        Tuple[Sequence[TransactionRow], str]:
            - transactions (Sequence[TransactionRow]): Sequence of transactions matching the type
            - title (str): Table title string describing the type
    """
    transaction_type = input_transaction_type(
        "Enter the transaction type (I)ncome or (E)xpense: "
    )
    transactions = retrieve_transactions_by_type(transaction_type)
    title = f"{transaction_type} transactions"
    return transactions, title


def action_quit():
    """
    Quit the retrieval interface.

    Returns:
        Tuple[None, None]: Indicates no transactions to display and exit signal
    """
    return None, None


RETRIEVE_ACTIONS = {
    1: action_all_transactions,
    2: action_by_date_range,
    3: action_by_amount_range,
    4: action_by_type,
    5: action_quit,
}
