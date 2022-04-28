from enum import Enum
from lib2to3.pgen2 import token
from typing import Dict, List, Union

from pydantic import BaseModel
from solanalib.constants import Marketplace
from solanalib.util import SafeDict
from solanalib.logger import logger


class Transaction(BaseModel):
    transaction_id: str
    block_time: int
    slot: int
    instructions: Instructions
    pre_token_balances: List[SafeDict]
    post_token_balances: List[SafeDict]
    accounts: Dict[int, SafeDict]

    def __init__(self, transaction: dict, *args, **kwargs):
        super().__init__(
            transaction_id=transaction["transaction"]["signatures"][0],
            block_time=transaction["blockTime"],
            slot=transaction["slot"],
            instructions=Instructions(transaction),
            pre_token_balances=[
                SafeDict(bal) for bal in transaction["meta"]["preTokenBalances"]
            ],
            post_token_balances=[
                SafeDict(bal) for bal in transaction["meta"]["postTokenBalances"]
            ],
            accounts={
                index: SafeDict(acc)
                for index, acc in enumerate(
                    transaction["transaction"]["message"]["accountKeys"]
                )
            },
            *args,
            **kwargs,
        )

    def get_account(self, index):
        if index in self.accounts:
            return self.accounts[index]["pubkey"]

    def get_owner(self, token_balance: SafeDict):
        if "owner" in token_balance:
            return token_balance["owner"]
        if "accountIndex" in token_balance:
            return self.get_account(token_balance["accountIndex"])
        return None

    def get_pre_owner(self, mint: str) -> Union[str, None]:
        for token_balance in self.pre_token_balances:
            if (
                token_balance["mint"] == mint
                and token_balance["uiTokenAmount"]["amount"] == "1"
            ):
                return self.get_owner(token_balance)
        return None

    def get_all_pre_owners(self, mint: str) -> List:
        owners = []
        for token_balance in self.pre_token_balances:
            if token_balance["mint"] == mint:
                owners.append(self.get_owner(token_balance))
        return owners

    def get_post_owner(self, mint: str) -> Union[str, None]:
        for token_balance in self.post_token_balances:
            if (
                token_balance["mint"] == mint
                and token_balance["uiTokenAmount"]["amount"] == "1"
            ):
                return self.get_owner(token_balance)
        return None

    def get_all_post_owners(self, mint: str) -> List:
        owners = []
        for token_balance in self.post_token_balances:
            if token_balance["mint"] == mint:
                owners.append(self.get_owner(token_balance))
        return owners
