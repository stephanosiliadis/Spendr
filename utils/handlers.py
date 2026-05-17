# Import local packages.
from utils.io import *
from utils.db import (
    insert_transaction,
    retrieve_transaction,
    delete_transaction,
    update_transaction,
    retrieve_transactions,
    save_transactions,
)
from models.Transaction import Transaction
from utils.retrieveactions import RETRIEVE_ACTIONS
from utils.parsetransactiondate import parse_transaction_date


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
    description = safe_input("Enter the description of the transaction: ")
    while description.strip() == "":
        print("Invalid Option: transaction description cannot be left empty.")
        description = safe_input("Enter the description of the transaction: ")

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

        # Ask the user if they want to save the retrieved transactions,
        # only if the did not pick to retrieve all transactions.
        if choice != 1:
            while True:
                save_choice = (
                    safe_input("Do you want to save the retrieved transactions (y/n): ")
                    .strip()
                    .lower()
                )

                if save_choice in ("y", "yes"):
                    # Ask for format
                    header = "Save as:"
                    actions = ["CSV", "JSON", "Excel", "Database File"]
                    extension_choice = print_actions(header, actions)

                    if extension_choice == 1:
                        save_transactions(transactions, "CSV", title)
                    elif extension_choice == 2:
                        save_transactions(transactions, "JSON", title)
                    elif extension_choice == 3:
                        save_transactions(transactions, "Excel", title)
                    else:
                        save_transactions(transactions, "Database File", title)
                    break

                elif save_choice in ("n", "no"):
                    print("[INFO] Skipping save...")
                    break

                else:
                    print("Invalid Option: Please enter (y)es or (n)o.")
    else:
        print("[INFO] No transactions found...")


def delete_single_transaction():
    # Header.
    print("=== DELETE A SINGLE TRANSACTION ===")
    print()

    # Get the id of the transaction.
    transaction_id = 0
    while True:
        transaction_id = safe_input(
            "Enter the ID of the transaction you want to delete: "
        )
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
        print("[INFO] No transactions with the specified ID where found...")
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
        print(f"[INFO] Transaction with id={transaction_id} successfully deleted...")
    else:
        print("Aborting deletion process...")
        return


def _input_optional_transaction_type(message: str, current_value: str) -> str:
    transaction_type = safe_input(message).strip()
    while transaction_type != "" and transaction_type.lower() not in (
        "i",
        "e",
        "income",
        "expense",
    ):
        print("Invalid Option: for the type of the transaction.")
        transaction_type = safe_input(message).strip()

    if transaction_type == "":
        return current_value
    if transaction_type.lower() in ("i", "income"):
        return "Income"
    return "Expense"


def _input_optional_transaction_amount(message: str, current_value: float) -> float:
    while True:
        amount = safe_input(message).strip()
        if amount == "":
            return current_value
        try:
            amount = float(amount)
            if amount > 0:
                return amount
            print("Invalid Option: transaction amount must be a positive number.")
        except ValueError:
            print("Invalid Option: Please enter a number.")


def _input_optional_transaction_date(message: str, current_value):
    while True:
        date_input = safe_input(message).strip()
        if date_input == "":
            return parse_transaction_date(str(current_value))
        try:
            return parse_transaction_date(date_input)
        except ValueError:
            print(
                "Invalid Option: Unable to parse date. Try something like 'today', 'yesterday', or '2026-03-10'."
            )


def _input_transaction_edits(transaction: tuple) -> Transaction:
    _, current_type, current_amount, current_description, current_date = transaction

    print("Enter new values for the fields you want to edit.")
    print("Press ENTER without typing a value to keep the current value.")

    transaction_type = _input_optional_transaction_type(
        f"Enter the new type ({current_type}) (I)ncome or (E)xpense: ",
        current_type,
    )
    amount = _input_optional_transaction_amount(
        f"Enter the new amount ({current_amount}): ",
        current_amount,
    )
    description = safe_input(
        f"Enter the new description ({current_description}): "
    ).strip()
    if description == "":
        description = current_description
    transaction_date = _input_optional_transaction_date(
        f"Enter the new date ({current_date}) YYYY-MM-DD: ",
        current_date,
    )

    return Transaction(transaction_type, amount, description, transaction_date)


def edit_existing_transaction(transaction_id: int):
    # First select the transaction to confirm that it is the correct one.
    transaction = retrieve_transaction(transaction_id)

    print()
    if not transaction:
        print("[INFO] No transactions with the specified ID where found...")
        return

    # Transaction exists.
    display_transactions(transaction, "You will edit the following transaction:")
    ok = input(
        f"Proceed with the edit of the transaction with id={transaction_id} (y/n): "
    )
    while ok.lower() not in ("yes", "y", "no", "n"):
        print("Invalid Option: Please enter (y)es or (n)o.")
        ok = input(
            f"Proceed with the edit of the transaction with id={transaction_id} (y/n): "
        )

    print()
    if ok.lower() not in ("yes", "y"):
        print("Aborting edit process...")
        return

    updated_transaction = _input_transaction_edits(transaction[0])
    update_transaction(transaction_id, updated_transaction)
    updated_transaction_row = retrieve_transaction(transaction_id)

    print()
    display_transactions(updated_transaction_row, "Transaction updated:")


def edit_single_transaction():
    # Header.
    print("=== EDIT A SINGLE TRANSACTION ===")
    print()

    # Get the id of the transaction.
    transaction_id = 0
    while True:
        transaction_id = safe_input("Enter the ID of the transaction you want to edit: ")
        try:
            transaction_id = int(transaction_id)
            if transaction_id >= 0:
                break
            else:
                print("Invalid Option: transaction id must be non-negative.")
        except ValueError:
            print("Invalid Option: Please enter a number.")

    edit_existing_transaction(transaction_id)


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
        print("\n[INFO] No transactions found in the database...\n")
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
