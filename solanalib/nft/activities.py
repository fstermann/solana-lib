from enum import Enum
from typing import Union

from pydantic import BaseModel  # noqa


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
    old_token_account: Union[str, None] = None
    new_token_account: Union[str, None] = None
    old_authority: Union[str, None] = None  # -> old_authority, transfered from
    new_authority: Union[str, None] = None  # -> buyer, minter, transfered to
    program: Union[str, None] = None

    def __hash__(self):
        return hash(self.transaction_id)


class UnknownActivity(Activity):
    type_: ActivityType = ActivityType.UNKNOWN


class MintActivity(Activity):
    type_: ActivityType = ActivityType.MINT


class ListingActivity(Activity):
    price_lamports: int

    type_: ActivityType = ActivityType.LISTING


class TransferActivity(Activity):

    type_: ActivityType = ActivityType.TRANSFER


class DelistingActivity(Activity):
    type_: ActivityType = ActivityType.DELISTING


class SaleActivity(Activity):
    price_lamports: int

    type_: ActivityType = ActivityType.SALE
