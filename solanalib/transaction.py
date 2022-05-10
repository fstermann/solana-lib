from typing import Dict, Union

from pydantic import BaseModel  # noqa

from solanalib.nft.instructions import Instructions
from solanalib.util import SafeDict


class Transaction(BaseModel):
    transaction_id: str
    block_time: int
    slot: int
    instructions: Instructions
    accounts: Dict[int, SafeDict]

    def __init__(self, transaction: dict, *args, **kwargs):
        super().__init__(
            transaction_id=transaction["transaction"]["signatures"][0],
            block_time=transaction["blockTime"],
            slot=transaction["slot"],
            instructions=Instructions(transaction),
            accounts={
                index: SafeDict(acc)
                for index, acc in enumerate(
                    transaction["transaction"]["message"]["accountKeys"]
                )
            },
            *args,
            **kwargs,
        )

    def __hash__(self):
        return hash(self.transaction_id)

    @property
    def account_keys(self):
        return [account["pubkey"] for account in self.accounts.values()]

    def get_account(self, index) -> Union[str, None]:
        if index in self.accounts:
            return self.accounts[index]["pubkey"]
        return None


class NFTTransaction(Transaction):
    mint: str
