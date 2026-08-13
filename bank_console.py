"""
SecureBank - Week 2
In-memory CLI ledger with transaction history.
"""

from dataclasses import dataclass, field
from datetime import datetime


class AccountNotFoundError(Exception):
    """Raised when an operation targets an account ID that doesn't exist (or was closed)."""
    pass


class InsufficientFundsError(Exception):
    """Raised when a withdrawal amount exceeds the account's current balance."""
    pass


@dataclass
class Transaction:
    type: str
    amount: float
    timestamp: datetime


@dataclass
class Account:
    id: int
    customer_name: str
    balance: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)


accounts: dict[int, Account] = {}
_next_id = 1


def create_account(customer_name: str) -> Account:
    global _next_id

    account = Account(
        id=_next_id,
        customer_name=customer_name,
        balance=0.0
    )

    accounts[_next_id] = account
    _next_id += 1

    return account


def _get_account(account_id: int) -> Account:
    """Internal helper: look up an account, or raise AccountNotFoundError."""
    if account_id not in accounts:
        raise AccountNotFoundError(
            f"No account found with ID {account_id}."
        )

    return accounts[account_id]


def deposit(account_id: int, amount: float) -> Account:
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")

    account = _get_account(account_id)

    account.balance += amount

    account.transactions.append(
        Transaction(
            type="deposit",
            amount=amount,
            timestamp=datetime.now()
        )
    )

    return account


def withdraw(account_id: int, amount: float) -> Account:
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")

    account = _get_account(account_id)

    if amount > account.balance:
        raise InsufficientFundsError(
            f"Cannot withdraw ₹{amount:.2f}. "
            f"Account {account_id} balance is only ₹{account.balance:.2f}."
        )

    account.balance -= amount

    account.transactions.append(
        Transaction(
            type="withdraw",
            amount=amount,
            timestamp=datetime.now()
        )
    )

    return account


def check_balance(account_id: int) -> float:
    account = _get_account(account_id)
    return account.balance


def get_transactions(account_id: int) -> list[Transaction]:
    account = _get_account(account_id)
    return account.transactions


def close_account(account_id: int) -> None:
    _get_account(account_id)
    del accounts[account_id]


MENU = """
==== SecureBank ====
1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. Close Account
6. List All Accounts
7. View Transactions
0. Exit
"""


def run_cli():
    print("Welcome to SecureBank.")

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Customer name: ").strip()

                acc = create_account(name)

                print(
                    f"Created account {acc.id} "
                    f"for {acc.customer_name}."
                )

            elif choice == "2":
                acc_id = int(input("Account ID: "))
                amt = float(input("Deposit amount: "))

                acc = deposit(acc_id, amt)

                print(
                    f"Deposited ₹{amt:.2f}. "
                    f"New balance: ₹{acc.balance:.2f}"
                )

            elif choice == "3":
                acc_id = int(input("Account ID: "))
                amt = float(input("Withdraw amount: "))

                acc = withdraw(acc_id, amt)

                print(
                    f"Withdrew ₹{amt:.2f}. "
                    f"New balance: ₹{acc.balance:.2f}"
                )

            elif choice == "4":
                acc_id = int(input("Account ID: "))

                bal = check_balance(acc_id)

                print(
                    f"Balance for account {acc_id}: "
                    f"₹{bal:.2f}"
                )

            elif choice == "5":
                acc_id = int(input("Account ID: "))

                close_account(acc_id)

                print(f"Account {acc_id} closed.")

            elif choice == "6":
                if not accounts:
                    print("No accounts yet.")

                for acc in accounts.values():
                    print(
                        f"[{acc.id}] "
                        f"{acc.customer_name} - "
                        f"₹{acc.balance:.2f}"
                    )

            elif choice == "7":
                acc_id = int(input("Account ID: "))

                transactions = get_transactions(acc_id)

                if not transactions:
                    print("No transactions yet.")

                else:
                    for transaction in transactions:
                        print(
                            f"{transaction.timestamp} - "
                            f"{transaction.type}: "
                            f"₹{transaction.amount:.2f}"
                        )

            elif choice == "0":
                print("Goodbye.")
                break

            else:
                print("Invalid option. Try again.")

        except AccountNotFoundError as e:
            print(f"Error: {e}")

        except InsufficientFundsError as e:
            print(f"Error: {e}")

        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    run_cli()