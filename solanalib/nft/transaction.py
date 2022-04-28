from typing import Callable, Dict, List, Optional, Union

from pydantic import BaseModel
from solanalib.logger import logger
from solanalib.nft.activities import Activity
from solanalib.util import SafeDict

from .instructions import Instructions


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

    def parse_ixs(
        self, parser: Callable, with_inner: Optional[bool] = False
    ) -> Union[Activity, None]:
        for index, ix in enumerate(self.instructions.outer):
            activity = parser(ix=ix)
            if activity:
                return activity

            if not with_inner:
                continue
            if ix.is_parsed:
                continue
            if not index in self.instructions.inner:
                continue

            for iix in self.instructions.inner[index]:
                activity = parser(ix=iix)
                if activity:
                    return activity

        return None

    def get_mint_by_accounts(self, *args) -> Union[str, None]:
        for token_balance in self.pre_token_balances:
            if self.get_owner(token_balance) in args:
                return token_balance["mint"]
        for token_balance in self.post_token_balances:
            if self.get_owner(token_balance) in args:
                return token_balance["mint"]
        return None

    @property
    def account_keys(self):
        return [account["pubkey"] for account in self.accounts.values()]

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


class NFTTransaction(Transaction):
    mint: str
