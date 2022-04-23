from typing import Union

from solanalib.constants import AuctionHouse, MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.models import ListingActivity, Transaction

from .util import get_me_lamports_price_from_data


def parse_listing_mev1(tx: Transaction, mint: str) -> Union[ListingActivity, None]:
    for index, ix in enumerate(tx.instructions.outer):
        if not ix.is_program_id(MagicEdenV1.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV1.NAME}")
        marketplace = MagicEdenV1.MARKETPLACE

        if ix.data[0:10] == MagicEdenV1.LISTING_INSTRUCTION:
            logger.debug("Is Listing instruction")

            old_authority = ix["accounts"][0]  # 1st account
            old_token_account = ix["accounts"][1]
            listing_price = get_me_lamports_price_from_data(
                ix.data, MagicEdenV1.PROGRAM
            )

            new_authority = None
            for iix in tx.instructions.inner[index]:
                if (
                    iix.is_type("setAuthority")
                    and iix.info["account"] == old_token_account
                ):
                    new_authority = iix.info["newAuthority"]

            return ListingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                old_authority=old_authority,
                new_authority=new_authority,
                old_token_account=old_token_account,
                new_token_account=old_token_account,  # In MEv1 token account doesn't change
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

            old_authority = ix["accounts"][0]  # 1st account
            listing_price = get_me_lamports_price_from_data(
                ix.data, MagicEdenV2.PROGRAM
            )

            return ListingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                old_authority=old_authority,
                price_lamports=listing_price,
                marketplace=marketplace,
            )
    return None


def parse_listing_auction_house(
    tx: Transaction, mint: str
) -> Union[ListingActivity, None]:
    for ix in tx.instructions.outer:
        if not ix.is_program_id(AuctionHouse.PROGRAM):
            continue
        logger.debug(f"Program is {AuctionHouse.NAME}")
        marketplace = AuctionHouse.MARKETPLACE

        if ix.data[0:10] == AuctionHouse.LISTING_INSTRUCTION:
            logger.debug("Is Listing instruction")

            old_authority = ix["accounts"][0]  # 1st account
            listing_price = get_me_lamports_price_from_data(
                ix.data, AuctionHouse.PROGRAM
            )

            return ListingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                old_authority=old_authority,
                price_lamports=listing_price,
                marketplace=marketplace,
            )
    return None


def parse_listing(tx: Transaction, mint: str) -> Union[ListingActivity, None]:
    to_parse = {
        "MagiEdenV1": parse_listing_mev1,
        "MagiEdenV2": parse_listing_mev2,
        "AuctionHouse": parse_listing_auction_house,
    }

    for marketplace, parser in to_parse.items():
        logger.info(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
