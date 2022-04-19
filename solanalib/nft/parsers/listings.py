from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.models import ListingActivity, Transaction

from .util import get_me_lamports_price_from_data


def parse_listing_mev1(tx: Transaction, mint: str) -> Union[ListingActivity, None]:
    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV1.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV1.NAME}")
        marketplace = MagicEdenV1.MARKETPLACE

        if ix.data[0:10] == MagicEdenV1.LISTING_INSTRUCTION:
            logger.debug("Is Listing instruction")

            seller = ix["accounts"][0]  # 1st account
            listing_price = get_me_lamports_price_from_data(
                ix.data, MagicEdenV1.PROGRAM
            )

            return ListingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                seller=seller,
                price_lamports=listing_price,
                marketplace=marketplace,
            )
    return None


def parse_listing_mev2(tx: Transaction, mint: str) -> Union[ListingActivity, None]:
    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV2.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV2.NAME}")
        marketplace = MagicEdenV2.MARKETPLACE

        if ix.data[0:10] == MagicEdenV2.LISTING_INSTRUCTION:
            logger.debug("Is Listing instruction")
            if ix["accounts"][4] != mint:  # 5th account
                logger.debug("Mint did not match")

            seller = ix["accounts"][0]  # 1st account
            listing_price = get_me_lamports_price_from_data(
                ix.data, MagicEdenV2.PROGRAM
            )

            return ListingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                seller=seller,
                price_lamports=listing_price,
                marketplace=marketplace,
            )
    return None


def parse_listing(tx: Transaction, mint: str) -> Union[ListingActivity, None]:
    to_parse = {
        "MagiEdenV1": parse_listing_mev1,
        "MagiEdenV2": parse_listing_mev2,
    }

    for marketplace, parser in to_parse.items():
        logger.info(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
