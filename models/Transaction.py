# Import standard library packages.
from datetime import date
from dataclasses import dataclass


@dataclass
class Transaction:
    """
    A class to represent a Transaction in the database

    Attributes:
            id (int): The unique ID of the Transaction.
            type (str): The type of the Transaction (Expense or Income)
            amount (float): The amount that the Transaction describes.
            description (str): A short description of what is that Transaction.
            date (date): The date that the Transaction happened.
    """

    type: str
    amount: float
    description: str
    date: date

    def __repr__(self) -> str:
        return f"{self.type} of {self.amount}€ on {self.date} for {self.description}"
