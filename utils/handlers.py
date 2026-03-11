# Import local packages.
from utils.io import *
from utils.db import (
    insert_transaction,
    retrieve_transaction,
    delete_transaction,
    retrieve_transactions,
)
from models.Transaction import Transaction
from utils.retrieveactions import RETRIEVE_ACTIONS


def insert_new_transaction():
    # Header.
    print("=== INSERT NEW TRANSACTION ===")
    print("Enter the details of the new transaction below:")

    # ---------- T Y P E ----------
    transaction_type = input_transaction_type(
        "Enter the type of the transaction, an (I)ncome or an (E)xpense: "
    )

    # ---------- A M O U N T ----------
    amount = input_transaction_amount("Enter the amount of the transaction: ")

    # ---------- D E S C R I P T I O N ----------
    description = input("Enter the description of the transaction: ")
    while description.strip() == "":
        print("Invalid Option: transaction description cannot be left empty.")
        description = input("Enter the description of the transaction: ")

    # ---------- D A T E ----------
    transaction_date = input_transaction_date(
        "Enter the date YYYY-MM-DD of the transaction (press ENTER for today): "
    )

    # Create the Transaction instance.
    transaction = Transaction(transaction_type, amount, description, transaction_date)

    # Insert it.
    insert_transaction(transaction)

    transactions = retrieve_transactions()
    if transactions:
        transaction_row = retrieve_transaction(transactions[-1][0])

        # Print it to the console.
        display_transactions(transaction_row, "Transaction created:")


def retrieve_past_transactions():
    # Header.
    print("=== RETRIEVE PAST TRANSACTIONS ===")

    # Show retrieval actions and get the user's choice.
    header = "How would you like to retrieve transactions?"
    actions = [
        "All transactions",
        "Transactions within a date range",
        "Transactions within an amount range",
        "Transactions by type (Income/Expense)",
        "Back to main menu",
    ]
    choice = print_actions(header, actions)

    # Perform the chosen action.
    action_func = RETRIEVE_ACTIONS.get(choice)
    if action_func is None:
        print("Invalid choice.")
        return

    transactions, title = action_func()

    # Display the retrieved Transactions.
    print()
    if transactions:
        display_transactions(transactions, title)
    else:
        print("[INFO] No transactions found.")


def delete_single_transaction():
    # Header.
    print("=== DELETE A SINGLE TRANSACTION ===")
    print()

    # Get the id of the transaction.
    transaction_id = 0
    while True:
        transaction_id = input("Enter the ID of the transaction you want to delete: ")
        try:
            transaction_id = int(transaction_id)
            if transaction_id >= 0:
                break
            else:
                print("Invalid Option: transaction id must be non-negative.")
        except ValueError:
            print("Invalid Option: Please enter a number.")

    # First select the transaction to confirm that it is the correct one.
    transaction = retrieve_transaction(transaction_id)

    print()
    if not transaction:
        print("[INFO] No transactions with the specified ID where found.")
        return

    # Transaction exists.
    display_transactions(transaction, "You will delete the following transaction:")
    ok = input(
        f"Proceed with the deletion of the transaction with id={transaction_id} (y/n): "
    )
    while ok.lower() not in ("yes", "y", "no", "n"):
        print("Invalid Option: Please enter (y)es or (n)o.")
        ok = input(
            f"Proceed with the deletion of the transaction with id={transaction_id} (y/n): "
        )

    # Delete or not the transaction.
    print()
    if ok.lower() in ("yes", "y"):
        delete_transaction(transaction_id)
        print(f"[INFO] Transaction with id={transaction_id} successfully deleted.")
    else:
        print("Aborting deletion process...")
        return


def get_transaction_insights():
    """
    Display key insights for all transactions in the database
    in a single Rich table with color-coded amounts.

    Insights include:
        - Total Income
        - Total Expenses
        - Net Balance
        - Highest Income
        - Highest Expense
        - Average Transaction Amount
    """

    # Retrieve all transactions
    transactions = retrieve_transactions()

    if not transactions:
        print("\n[INFO] No transactions found in the database.\n")
        return

    # Split transactions by type
    income_transactions = [t for t in transactions if t[1].lower() == "income"]
    expense_transactions = [t for t in transactions if t[1].lower() == "expense"]

    # Compute insights
    total_income = sum(t[2] for t in income_transactions)
    total_expenses = sum(t[2] for t in expense_transactions)
    net_balance = total_income - total_expenses

    highest_income = max(income_transactions, key=lambda t: t[2], default=None)
    highest_expense = max(expense_transactions, key=lambda t: t[2], default=None)

    all_amounts = [t[2] for t in transactions]
    average_amount = sum(all_amounts) / len(all_amounts) if all_amounts else 0

    # Create Rich console and table
    console = Console()
    table = Table(
        title="Transaction Insights", box=box.ROUNDED, header_style="bold white"
    )

    table.add_column("Insight", style="bold white")
    table.add_column("Value", justify="right", style="bold")

    # Add rows with color coding
    table.add_row("Total Income", f"[green]+{total_income:.2f}€[/green]")
    table.add_row("Total Expenses", f"[red]-{total_expenses:.2f}€[/red]")
    net_color = "green" if net_balance >= 0 else "red"
    table.add_row("Net Balance", f"[{net_color}]{net_balance:.2f}€[/{net_color}]")

    if highest_income:
        table.add_row(
            "Highest Income",
            f"[green]+{highest_income[2]:.2f}€[/green] ({highest_income[3]} on {highest_income[4]})",
        )
    else:
        table.add_row("Highest Income", "[green]N/A[/green]")

    if highest_expense:
        table.add_row(
            "Highest Expense",
            f"[red]-{highest_expense[2]:.2f}€[/red] ({highest_expense[3]} on {highest_expense[4]})",
        )
    else:
        table.add_row("Highest Expense", "[red]N/A[/red]")

    table.add_row("Average Transaction", f"{average_amount:.2f}€")

    # Print the table
    console.print(table)
