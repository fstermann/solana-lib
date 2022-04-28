from enum import Enum
from typing import Union

from pydantic import BaseModel


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
    mint: Union[str, None] = None
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
