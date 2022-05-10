from typing import List

from pydantic import BaseModel  # noqa

from solanalib.nft.instructions import Instruction

from .transaction import Transaction


class SolTransfer(BaseModel):
    source: str
    destination: str
    amount: int
    program: str

    def __init__(self, ix: Instruction, *args, program: str = None, **kwargs):
        if not program:
            program = ix["program"]
        super().__init__(
            source=ix.info["source"],
            destination=ix.info["destination"],
            amount=ix.info["lamports"],
            program=program,
            *args,
            **kwargs,
        )


class TransferTransaction(Transaction):
    pre_balances: List[int]
    post_balances: List[int]

    def __init__(self, transaction: dict, *args, **kwargs):
        super().__init__(
            transaction=transaction,
            pre_balances=transaction["meta"]["preBalances"],
            post_balances=transaction["meta"]["postBalances"],
            *args,
            **kwargs,
        )

    def parse_sol_transfers(self, account: str = None) -> List[SolTransfer]:
        def account_in_ix(ix: Instruction) -> bool:
            if not account:
                return True
            return account in (
                ix.info["source"],
                ix.info["destination"],
            )

        transfers = []

        for index, ix in enumerate(self.instructions.outer):
            if ix.is_sol_transfer() and account_in_ix(ix=ix):
                transfers.append(SolTransfer(ix=ix))

            if ix.is_parsed:
                continue
            if index not in self.instructions.inner:
                continue

            for iix in self.instructions.inner[index]:
                if iix.is_sol_transfer() and account_in_ix(ix=iix):
                    transfers.append(SolTransfer(ix=iix, program=ix["programId"]))

        return transfers
