from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.models import ListingActivity, Transaction

from .util import get_me_listing_price_from_data


def check_listing_me(
    magic_eden: Union[MagicEdenV1, MagicEdenV2], tx: Transaction, mint: str
) -> Union[ListingActivity, None]:
    me_program_check = False
    me_authority_check = False

    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_program_id(magic_eden.PROGRAM):
            logger.debug(f"Is program {magic_eden.NAME}")

            for iix in tx.instructions.inner[index]:
                if iix.is_create_account_by_program(magic_eden.PROGRAM):
                    me_program_check = True
                if iix.is_set_authority() and iix.is_new_authority(
                    magic_eden.AUTHORITY
                ):
                    me_authority_check = True
                    listing_authority = iix.authority
                    marketplace = magic_eden.MARKETPLACE

                    if ix.has_data():
                        listing_price = get_me_listing_price_from_data(
                            ix.data, magic_eden.PROGRAM
                        )

    if me_program_check & me_authority_check:
        logger.debug("Is listing tx")
        return ListingActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            listing_authority=listing_authority,
            price_lamports=listing_price,
            marketplace=marketplace,
        )
    return None


def parse_listing(tx: Transaction, mint: str):
    activity = check_listing_me(magic_eden=MagicEdenV1, tx=tx, mint=mint)
    if activity:
        return activity

    activity = check_listing_me(magic_eden=MagicEdenV2, tx=tx, mint=mint)
    if activity:
        return activity

    return None
