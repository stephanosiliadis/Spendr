# Import standard library packages.
from datetime import date, datetime

# Import third-party packages.
from rich import box
from rich.table import Table
from rich.console import Console

# Import local packages.
from utils.exceptions import QuitToMenu
from utils.parsetransactiondate import parse_transaction_date


def safe_input(prompt: str) -> str:
    value = input(prompt).strip()

    if value.lower() == "q":
        raise QuitToMenu()

    return value


def print_actions(header: str, actions: list[str]) -> int:
    """
    Print a menu and return the user's choice.

    Args:
        header (str): The header message shown above the actions.
        actions (list[str]): A list of actions to display.

    Returns:
        choice (int): The number corresponding to the selected action.
    """
    print(f"\n{header}")

    # Print numbered actions
    for i, action in enumerate(actions, start=1):
        print(f"{i}. {action}")

    max_choice = len(actions)

    # Input validation loop
    while True:
        choice = input(f"Enter your choice (1-{max_choice}): ")
        try:
            choice = int(choice)
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(f"Invalid Option: Choose a number from 1 to {max_choice}.")
        except ValueError:
            print("Invalid Option: Please enter a number.")


def input_transaction_type(message: str) -> str:
    """
    Prompt the user to input the type of a transaction.

    The user must enter either Income or Expense. The function accepts
    several variations such as "I", "E", "income", or "expense" (case-insensitive)
    and normalizes the result to either "Income" or "Expense".

    Args:
        message (str): The prompt message displayed to the user.

    Returns:
        transaction_type (str): The normalized transaction type, either "Income" or "Expense".
    """
    transaction_type = safe_input(message)
    while transaction_type.lower() not in ("i", "e", "income", "expense"):
        print("Invalid Option: for the type of the transaction.")
        transaction_type = safe_input(message)

    # Normalize type.
    if transaction_type.lower() in ("i", "income"):
        transaction_type = "Income"
    else:
        transaction_type = "Expense"

    return transaction_type


def input_transaction_amount(message: str) -> float:
    """
    Prompt the user to input the transaction amount.

    The function repeatedly asks for input until the user provides a valid
    positive number. Any non-numeric input or non-positive values will
    trigger an error message and another prompt.

    Args:
        message (str): The prompt message displayed to the user.

    Returns:
        amount (float): A positive number representing the transaction amount.
    """
    amount = 0
    while True:
        amount = safe_input(message)
        try:
            amount = float(amount)
            if amount > 0:
                break
            else:
                print("Invalid Option: transaction amount must be a positive number.")
        except ValueError:
            print("Invalid Option: Please enter a number.")

    return amount


def input_transaction_date(message: str) -> date:
    """
    Prompt the user to input the date of a transaction.

    The user may enter a date in various natural formats (e.g. "2026-03-10",
    "March 10", "yesterday"). The input is parsed using the date parsing
    library and converted to a date object. If the user leaves the input
    empty, today's date is used.

    Args:
        message (str): The prompt message displayed to the user.

    Returns:
        transaction_date (date): A date object representing the transaction date.
    """
    transaction_date = 0
    while True:
        date_input = safe_input(message).strip()
        if date_input == "":
            transaction_date = datetime.today().date()
            break
        try:
            transaction_date = parse_transaction_date(date_input)
            break
        except ValueError:
            print(
                "Invalid Option: Unable to parse date. Try something like 'today', 'yesterday', or '2026-03-10'."
            )
    return transaction_date


def display_transactions(transactions: list[tuple], table_title: str) -> None:
    """
    Display a list of transactions in a styled Rich table.

    Each transaction is expected to be a tuple containing:
        (id, type, amount, description, date)

    The "Type" and "Amount" columns are color-coded:
        - Income -> green
        - Expense -> red
        Amounts include a "+" or "-" sign accordingly.

    Args:
        transactions (list[tuple]): List of transactions to display.
        table_title (str): The title to display at the top of the table.

    Returns:
        None
    """
    # Create Console and Table instances.
    console = Console()
    table = Table(
        title=f"{table_title}",
        header_style="white",
        box=box.ROUNDED,
    )

    # Create the columns.
    table.add_column("ID", justify="left", style="white", no_wrap=True)
    table.add_column("Type", justify="center")
    table.add_column("Amount", justify="center")
    table.add_column("Description", justify="center", style="white")
    table.add_column("Date", justify="center", style="white")

    # Fill the table.
    for transaction in transactions:
        t_id, t_type, amount, description, date = transaction

        # Decide on the proper color for the type and the amount values.
        if t_type.lower() == "expense":
            type_str = "[red]Expense[/red]"
            amount_str = f"[red]-{amount:.2f}€[/red]"
        else:
            type_str = "[green]Income[/green]"
            amount_str = f"[green]+{amount:.2f}€[/green]"

        # Add the row.
        table.add_row(
            str(t_id),
            type_str,
            amount_str,
            description,
            str(date),
        )

    # Print the table.
    console.print(table)
