# Import third-party packages.
import typer

# Import local packages.
from utils.handlers import *
from utils.io import print_actions
from utils.retrieveactions import RETRIEVE_ACTIONS
from utils.parsetransactiondate import parse_transaction_date
from utils.handlers import input_transaction_type, input_transaction_amount
from utils.db import create_db_tables, insert_transaction, delete_transaction


# Create app instance.
app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def menu(ctx: typer.Context):
    """Run the interactive SPENDR CLI menu."""
    if ctx.invoked_subcommand is None:
        # Print Welcome Header and available actions.
        print("=== SPENDR CLI ===")
        while True:
            header = "Available Actions:"
            actions = [
                "Insert new transaction",
                "Retrieve past transactions",
                "Delete single transaction",
                "Get transaction insights",
                "End Sesssion",
            ]
            choice = print_actions(header, actions)
            print()

            # Perform the necessary action using the handlers or exit.
            if choice == 1:
                insert_new_transaction()
            elif choice == 2:
                retrieve_past_transactions()
            elif choice == 3:
                delete_single_transaction()
            elif choice == 4:
                get_transaction_insights()
            else:
                break

        # Print final Header.
        print("=== SPENDR SESSION ENDED ===")


@app.command()
def add(
    type: str = typer.Option(
        None, "--type", "-t", help="Type of transaction (Income or Expense)"
    ),
    amount: float = typer.Option(
        None, "--amount", "-a", help="Amount of the transaction"
    ),
    description: str = typer.Option(
        None, "--description", "-d", help="Description of the transaction"
    ),
    date: str = typer.Option(
        None,
        "--date",
        "-D",
        help="Date of the transaction (YYYY-MM-DD or leave empty for today)",
    ),
):
    """
    Insert a new transaction. You can provide options or fill them interactively.
    """
    # Interactive fallback if any parameter is missing
    if type is None:
        type = input_transaction_type(
            "Enter the type of the Transaction ((I)ncome or (E)xpense): "
        )
    if amount is None:
        amount = input_transaction_amount("Enter the amount of the Transaction: ")
    if description is None:
        description = input("Enter the description of the Transaction: ")
        while description.strip() == "":
            print("Description cannot be empty.")
            description = input("Enter the description of the Transaction: ")

    # Parse the date using our helper
    transaction_date = parse_transaction_date(date)

    # Insert transaction
    transaction = Transaction(type, amount, description, transaction_date)
    insert_transaction(transaction)
    transactions = retrieve_transactions()
    if transactions:
        transaction_row = retrieve_transaction(transactions[-1][0])

        # Print it to the console.
        print()
        display_transactions(transaction_row, "Transaction created:")


@app.command()
def list():
    """Retrieve past transactions."""
    action_func = RETRIEVE_ACTIONS.get(1)
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


@app.command()
def delete(
    id: int = typer.Option(None, "--id", "-id", help="The ID of the transaction"),
):
    """Delete a single transaction."""
    transaction = retrieve_transaction(id)

    print()
    if not transaction:
        print("[INFO] No transactions with the specified ID where found.")
        return

    # Transaction exists.
    display_transactions(transaction, "You will delete the following transaction:")
    ok = input(f"Proceed with the deletion of the transaction with id={id} (y/n): ")
    while ok.lower() not in ("yes", "y", "no", "n"):
        print("Invalid Option: Please enter (y)es or (n)o.")
        ok = input(f"Proceed with the deletion of the transaction with id={id} (y/n): ")

    # Delete or not the transaction.
    print()
    if ok.lower() in ("yes", "y"):
        delete_transaction(id)
        print(f"[INFO] Transaction with id={id} successfully deleted.")
    else:
        print("Aborting deletion process...")
        return


@app.command()
def insights():
    """Display transaction insights."""
    print()
    get_transaction_insights()


if __name__ == "__main__":
    create_db_tables()
    app()
