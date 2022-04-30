from typing import Union

# from solanalib.constants import AuctionHouse
from solanalib.logger import logger
from solanalib.nft.activities import ListingActivity
from solanalib.nft.instructions import Instruction
from solanalib.nft.marketplaces import marketplaces
from solanalib.nft.transaction import Transaction

from .util import get_me_lamports_price_from_data


def parse_listing_mev1(tx: Transaction) -> Union[ListingActivity, None]:
    def parse_ix(ix: Instruction) -> Union[ListingActivity, None]:
        marketplace = marketplaces.magic_eden_v1

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.listing.base64_prefix:
            return None
        logger.debug("Is Listing instruction")

        account_indices = marketplace.instructions.listing.account_indices

        old_authority = ix["accounts"][account_indices.old_authority]
        new_authority = marketplace.authority
        old_token_account = ix["accounts"][account_indices.old_token_account]

        price_lamports = get_me_lamports_price_from_data(ix.data, marketplace.program)

        mint = tx.get_mint_by_accounts(old_authority, new_authority, old_token_account)

        return ListingActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            old_authority=old_authority,
            new_authority=new_authority,
            old_token_account=old_token_account,
            new_token_account=old_token_account,  # In MEv1 token account doesn't change
            price_lamports=price_lamports,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


def parse_listing_mev2(tx: Transaction) -> Union[ListingActivity, None]:
    def parse_ix(ix: Instruction) -> Union[ListingActivity, None]:
        marketplace = marketplaces.magic_eden_v2

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.listing.base64_prefix:
            return None
        logger.debug("Is Listing instruction")

        account_indices = marketplace.instructions.listing.account_indices

        mint = ix["accounts"][account_indices.mint]
        old_authority = ix["accounts"][account_indices.old_authority]
        new_authority = marketplace.authority
        old_token_account = ix["accounts"][account_indices.old_token_account]

        price_lamports = get_me_lamports_price_from_data(ix.data, marketplace.program)

        return ListingActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            old_authority=old_authority,
            new_authority=new_authority,
            old_token_account=old_token_account,
            new_token_account=old_token_account,  # In MEv2 token account doesn't change
            price_lamports=price_lamports,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


# def parse_listing_auction_house(
#     tx: Transaction, mint: str
# ) -> Union[ListingActivity, None]:
#     for ix in tx.instructions.outer:
#         if not ix.is_program_id(AuctionHouse.PROGRAM):
#             continue
#         logger.debug(f"Program is {AuctionHouse.NAME}")
#         marketplace = AuctionHouse.MARKETPLACE

#         if ix.data[0:10] == AuctionHouse.LISTING_INSTRUCTION:
#             logger.debug("Is Listing instruction")

#             old_authority = ix["accounts"][0]  # 1st account
#             listing_price = get_me_lamports_price_from_data(
#                 ix.data, AuctionHouse.PROGRAM
#             )

#             return ListingActivity(
#                 transaction_id=tx.transaction_id,
#                 block_time=tx.block_time,
#                 slot=tx.slot,
#                 mint=mint,
#                 old_authority=old_authority,
#                 price_lamports=listing_price,
#                 program=marketplace,
#             )
#     return None


def parse_listing(tx: Transaction) -> Union[ListingActivity, None]:
    to_parse = {
        "MagiEdenV1": parse_listing_mev1,
        "MagiEdenV2": parse_listing_mev2,
        # "AuctionHouse": parse_listing_auction_house,
    }

    for marketplace, parser in to_parse.items():
        logger.debug(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx)
        if activity:
            return activity

    return None
