import sys
from decimal import Decimal
from uuid import UUID, uuid4

from account.account import Account
from database.database import TransactionDatabase
from database.implementations.pandas_db import TransactionDatabasePandas
import os

from transaction.transaction import Transaction


def create_transaction(database: TransactionDatabase, source: UUID, target: UUID, brutto: Decimal, netto: Decimal, curr: str, status: str) -> None:
    transaction = Transaction(
        id_=uuid4(),
        source_account= source,
        target_account= target,
        balance_brutto= brutto,
        balance_netto= netto,
        currency=curr,
        status= status,
    )
    database.save(transaction)

if __name__ == "__main__":

    database = TransactionDatabasePandas()
    source = UUID(input('Enter Source Account ID: '))
    target = UUID(input('Enter Target Account ID: '))
    brutto = Decimal(input('Enter brutto: '))
    netto = Decimal(input('Enter netto: '))
    currency = input('Enter Currency: ')
    status = input('Enter Status: ')
    create_transaction(database=database, source=source, target=target, brutto=brutto, netto=netto, curr=currency, status=status)
    sys.exit(0)