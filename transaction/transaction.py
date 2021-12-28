from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass
class Transaction:
    id_: UUID
    source_account: UUID
    target_account: UUID
    balance_brutto: Decimal
    balance_netto: Decimal
    currency: str
    status: str

    def to_json(self) -> dict:
        return {
            "id": str(self.id_),
            "source_account": str(self.source_account),
            "target_account": str(self.target_account),
            "balance_brutto": str(self.balance_brutto),
            "balance_netto": str(self.balance_netto),
            "currency": str(self.currency),
            "status": str(self.status),
        }
    
    def transfer(self, source: UUID, target: UUID, balance: Decimal, amount: Decimal) -> None:
        self.status = "Transferring..."
        self.source_account = source
        self.target_account = target
        self.balance_brutto = amount
        self.balance_netto = balance - amount
        if self.balance_netto < balance:
            self.status = "Transferring finished"
        else:
            self.status = "Something wrong"
    
    def fill(self, source: UUID, target: UUID, balance: Decimal, amount: Decimal) -> None:
        self.status = "Filling..."
        self.source_account = source
        self.target_account = source
        self.balance_brutto = amount
        self.balance_netto = balance + amount
        if self.balance_netto > balance:
            self.status = "Filling finished"
        else:
            self.status = "Something wrong"
