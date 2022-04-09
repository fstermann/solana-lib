from pydantic import BaseModel
from enum import Enum
from typing import List, Dict
from solanalib.util import SafeDict


class Instructions(BaseModel):
    outer: List[SafeDict]
    inner: Dict[int, List[SafeDict]]

    def __init__(self, transaction: dict):
        super().__init__(
            outer=[
                SafeDict(ix)
                for ix in transaction["transaction"]["message"]["instructions"]
            ],
            inner={
                ix["index"]: [SafeDict(iix) for iix in ix["instructions"]]
                for ix in transaction["meta"]["innerInstructions"]
            },
        )


class Transaction(BaseModel):
    transaction_id: str
    block_time: int
    slot: int
    instructions: Instructions

    def __init__(self, transaction: dict):
        super().__init__(
            transaction_id=transaction["transaction"]["signatures"][0],
            block_time=transaction["blockTime"],
            slot=transaction["slot"],
            instructions=Instructions(transaction),
        )


class ActivityType(str, Enum):
    MINT = "mint"
    LISTING = "listing"
    TRANSFER = "transfer"
    DELISTING = "delisting"
    SALE = "sale"


class Activity(BaseModel):
    transaction_id: str
    block_time: int
    slot: int
    mint: str


class MintActivity(Activity):
    mint_authority: str

    type_: ActivityType = ActivityType.MINT


class ListingActivity(Activity):
    listing_authority: str
    price_lamports: int

    type_: ActivityType = ActivityType.LISTING


class TransferActivity(Activity):
    new_authority: str
    transfered_from_account: str

    type_: ActivityType = ActivityType.TRANSFER


class DelistingActivity(Activity):
    new_authority: str

    type_: ActivityType = ActivityType.DELISTING


class SaleActivity(Activity):
    new_authority: str
    price_lamports: int

    type_: ActivityType = ActivityType.SALE
