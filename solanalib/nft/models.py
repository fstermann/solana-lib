from enum import Enum
from lib2to3.pgen2 import token
from typing import Dict, List, Union

from pydantic import BaseModel
from solanalib.constants import Marketplace
from solanalib.util import SafeDict
from solanalib.logger import logger


class AccountInfo(SafeDict):
    @property
    def has_info(self):
        return self["result"]["value"] is not None

    @property
    def mint(self):
        return self["result"]["value"]["data"]["parsed"]["info"]["mint"]


class Instruction(SafeDict):
    @property
    def parsed(self) -> SafeDict:
        return self["parsed"]

    @property
    def info(self) -> SafeDict:
        return self.parsed["info"]

    def get_authority(self) -> Union[str, None]:
        if "authority" in self.info:
            return self.info["authority"]
        # if "multisigAuthority" in self.info:
        #     return self.info["multisigAuthority"]

        logger.debug("Authority not found in parsed tx")
        return None

    def is_type(self, ttype: str) -> bool:
        return self.parsed["type"] == ttype

    def is_program(self, program: str) -> bool:
        return self["program"] == program

    def is_program_id(self, program_id: str) -> bool:
        return self["programId"] == program_id

    def is_spl_token_transfer(self) -> bool:
        if not (self.is_program("spl-token") and self.parsed["type"] == "transfer"):
            return False
        logger.debug(f"Is program spl-token and type {self.parsed['type']}")

        if not self.info["amount"] == "1":
            return False
        logger.debug("Transferred amount 1")

        return True

    def is_spl_token_checked_transfer(self) -> bool:
        if not (
            self.is_program("spl-token") and self.parsed["type"] == "transferChecked"
        ):
            return False
        logger.debug(f"Is program spl-token and type {self.parsed['type']}")

        if not self.info["tokenAmount"]["amount"] == "1":
            return False
        logger.debug("Transferred amount 1")

        return True

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

    def is_close_account(self, account: str) -> bool:
        if not (
            self.is_program("spl-token")
            and self.is_type("closeAccount")
            and self.info["account"] == account
        ):
            return False
        logger.debug("Is close account")

        return True

    def is_set_authority_for_account(self, account: str) -> bool:
        return (
            self.is_type("setAuthority")
            and self.info["authorityType"] == "accountOwner"
            and self.is_program("spl-token")
            and self.info["account"] == account
        )


class OuterInstruction(Instruction):
    @property
    def is_parsed(self) -> bool:
        return "parsed" in self

    @property
    def data(self) -> SafeDict:
        return self["data"]

    def has_data(self) -> bool:
        return "data" in self

    def is_mint(self, mint: str) -> bool:
        return (
            self.is_type("mintTo")
            and self.is_program("spl-token")
            and self.info["mint"] == mint
        )


class InnerInstruction(Instruction):
    @property
    def authority(self) -> SafeDict:
        return self.info["authority"]

    @property
    def new_authority(self) -> SafeDict:
        return self.info["newAuthority"]

    @property
    def source(self) -> SafeDict:
        return self.info["source"]

    def is_create_account_by_program(self, program: str) -> bool:
        return (
            self.is_type("createAccount")
            and self.info["owner"] == program
            and self.is_program("system")
        )

    def is_authority(self, authority: str) -> bool:
        return self.authority == authority

    def is_new_authority(self, new_authority: str) -> bool:
        return self.new_authority == new_authority


class Instructions(BaseModel):
    outer: List[OuterInstruction]
    inner: Dict[int, List[InnerInstruction]]

    def __init__(self, transaction: dict):
        outer_ix = transaction["transaction"]["message"]["instructions"]
        if not outer_ix:
            outer_ix = []

        inner_ix = transaction["meta"]["innerInstructions"]
        if not inner_ix:
            inner_ix = []

        super().__init__(
            outer=[OuterInstruction(ix) for ix in outer_ix],
            inner={
                ix["index"]: [InnerInstruction(iix) for iix in ix["instructions"]]
                for ix in inner_ix
            },
        )


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
