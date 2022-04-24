from enum import Enum
from typing import Dict, List

from pydantic import BaseModel
from solanalib.constants import Marketplace
from solanalib.util import SafeDict
from solanalib.logger import logger


class OuterInstruction(SafeDict):
    @property
    def data(self) -> SafeDict:
        return self["data"]

    @property
    def parsed(self) -> SafeDict:
        return self["parsed"]

    @property
    def info(self) -> SafeDict:
        return self.parsed["info"]

    def has_data(self) -> bool:
        return "data" in self

    def is_program(self, program: str) -> bool:
        return self["program"] == program

    def is_program_id(self, program_id: str) -> bool:
        return self["programId"] == program_id

    def is_type(self, _type: str) -> bool:
        return self.parsed["type"] == _type

    def is_mint(self, mint: str) -> bool:
        return (
            self.is_type("mintTo")
            and self.is_program("spl-token")
            and self.info["mint"] == mint
        )

    def is_create_associate_account_for_mint(self, mint: str) -> bool:
        if not (
            self.is_program("spl-associated-token-account") and self.is_type("create")
        ):
            return False
        logger.debug("Is createNewTokenAccount")

        if not self.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_initialize_account_for_mint(self, mint: str) -> bool:
        if not (self.is_program("spl-token") and self.is_type("initializeAccount")):
            return False
        logger.debug("Is initializeAccount")

        if not self.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_spl_token_transfer(self) -> bool:
        if not (
            self.is_program("spl-token")
            and self.parsed["type"]
            in [
                "transferChecked",
                "transfer",
            ]
        ):
            return False
        logger.debug(f"Is program spl-token and type {self.parsed['type']}")

        if not self.info["amount"] == "1":
            return False
        logger.debug("Transferred amount 1")

        return True


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

    def __init__(self, transaction: dict, *args, **kwargs):
        super().__init__(
            transaction_id=transaction["transaction"]["signatures"][0],
            block_time=transaction["blockTime"],
            slot=transaction["slot"],
            instructions=Instructions(transaction),
            *args,
            **kwargs,
        )


class NFTTransaction(Transaction):
    mint: str


class ActivityType(str, Enum):
    MINT = "mint"
    LISTING = "listing"
    TRANSFER = "transfer"
    DELISTING = "delisting"
    SALE = "sale"
    UNKNOWN = "unknown"


class Activity(BaseModel):
    transaction_id: str
    block_time: int
    slot: int
    mint: str
    old_token_account: str = None
    new_token_account: str = None
    old_authority: str = None  # -> old_authority, transfered from
    new_authority: str = None  # -> buyer, minter, transfered to
    program: str = None

    def __hash__(self):
        return hash(self.transaction_id)


class UnknownActivity(Activity):
    type_: ActivityType = ActivityType.UNKNOWN.value


class MintActivity(Activity):
    type_: ActivityType = ActivityType.MINT.value


class ListingActivity(Activity):
    price_lamports: int

    type_: ActivityType = ActivityType.LISTING.value


class TransferActivity(Activity):

    type_: ActivityType = ActivityType.TRANSFER.value


class DelistingActivity(Activity):
    type_: ActivityType = ActivityType.DELISTING.value


class SaleActivity(Activity):
    price_lamports: int

    type_: ActivityType = ActivityType.SALE.value
