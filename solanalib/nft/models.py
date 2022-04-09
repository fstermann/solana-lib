from pydantic import BaseModel
from enum import Enum
from typing import List, Dict
from solanalib.util import SafeDict


class OuterInstruction(SafeDict):
    @property
    def data(self) -> SafeDict:
        return self["data"]

    def has_data(self) -> bool:
        return "data" in self

    def is_program(self, program: str) -> bool:
        return self["programId"] == program


class InnerInstruction(SafeDict):
    @property
    def parsed(self) -> SafeDict:
        return self["parsed"]

    @property
    def info(self) -> SafeDict:
        return self.parsed["info"]

    @property
    def authority(self) -> SafeDict:
        return self.info["authority"]

    @property
    def new_authority(self) -> SafeDict:
        return self.info["newAuthority"]

    @property
    def source(self) -> SafeDict:
        return self.info["source"]

    def is_type(self, type_: str) -> bool:
        return self.parsed["type"] == type_

    def is_program(self, program: str) -> bool:
        return self["program"] == program

    def is_create_account_by_program(self, program: str) -> bool:
        return (
            self.is_type("createAccount")
            and self.info["owner"] == program
            and self.is_program("system")
        )

    def is_set_authority(self) -> bool:
        return (
            self.is_type("setAuthority")
            and self.info["authorityType"] == "accountOwner"
            and self.is_program("spl-token")
        )

    def is_authority(self, authority: str) -> bool:
        return self.authority == authority

    def is_new_authority(self, new_authority: str) -> bool:
        return self.new_authority == new_authority


class Instructions(BaseModel):
    outer: List[OuterInstruction]
    inner: Dict[int, List[InnerInstruction]]

    def __init__(self, transaction: dict):
        super().__init__(
            outer=[
                OuterInstruction(ix)
                for ix in transaction["transaction"]["message"]["instructions"]
            ],
            inner={
                ix["index"]: [InnerInstruction(iix) for iix in ix["instructions"]]
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
