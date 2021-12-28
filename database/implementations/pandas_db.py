from typing import ByteString, List
from uuid import UUID, uuid4
import pandas as pd
from pandas import DataFrame
from account.account import Account
from database.database import AccountDatabase
from database.database import TransactionDatabase
from database.database import ObjectNotFound
import transaction
from transaction.transaction import Transaction


class AccountDatabasePandas(AccountDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = pd.DataFrame(columns=["id", "currency", "balance"])
        try:
            self._objects = pd.read_pickle("database.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def clear_all(self) -> None:
        self._objects = pd.DataFrame(columns=["id", "currency", "balance"])
        self._objects.to_pickle("database.pk")

    def _save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        if account.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != account.id_]

        new_row = pd.DataFrame({
            "id": [account.id_],
            "currency": [account.currency],
            "balance": [account.balance],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("database.pk")

    def get_objects(self) -> List[Account]:
        result = []
        for index, row in self._objects.iterrows():
            result.append(Account(
                id_=row["id"],
                currency=row["currency"],
                balance=row["balance"],
            ))
        return result

    def get_object(self, id_: UUID) -> Account:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            account = Account(
                id_=filtered["id"],
                currency=filtered["currency"],
                balance=filtered["balance"],
            )
            return account
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")


class TransactionDatabasePandas(TransactionDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = pd.DataFrame(columns=["id", "source_account", "target_account", "balance_brutto", "balance_netto", "currency", "status"])
        try:
            self._objects = pd.read_pickle("database.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def clear_all(self) -> None:
        self._objects = pd.DataFrame(columns=["id", "source_account", "target_account", "balance_brutto", "balance_netto", "currency", "status"])
        self._objects.to_pickle("database.pk")

    def _save(self, transaction: Transaction) -> None:
        if transaction.id_ is None:
            transaction.id_ = uuid4()

        if transaction.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != transaction.id_]

        new_row = pd.DataFrame({
            "id": [transaction.id_],
            "source_account": [transaction.source_account],
            "target_account": [transaction.target_account],
            "balance_brutto": [transaction.balance_brutto],
            "balance_netto": [transaction.balance_netto],
            "currency": [transaction.currency],
            "status": [transaction.status],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("database.pk")

    def get_objects(self) -> List[Transaction]:
        result = []
        for index, row in self._objects.iterrows():
            result.append(Transaction(
                id_=row["id"],
                source_account=row["source_account"],
                target_account=row["target_account"],
                balance_brutto=row["balance_brutto"],
                balance_netto=row["balance_netto"],
                currency=row["currency"],
                status=row["status"],
            ))
        return result

    def get_object(self, id_: UUID) -> Transaction:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            transaction = Transaction(
                id_=filtered["id"],
                source_account=filtered["source_account"],
                target_account=filtered["target_account"],
                balance_brutto=filtered["balance_brutto"],
                balance_netto=filtered["balance_netto"],
                currency=filtered["currency"],
                status=filtered["status"],
            )
            return transaction
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")
