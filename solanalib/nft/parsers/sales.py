from typing import Union

from solanalib.logger import logger
from solanalib.nft.activities import SaleActivity
from solanalib.nft.instructions import Instruction
from solanalib.nft.marketplaces import marketplaces
from solanalib.nft.nft_transaction import NftTransaction

from .util import get_me_lamports_price_from_data

# def parse_sale_unknown(tx: NftTransaction, mint: str) -> Union[SaleActivity, None]:
#     transfer_activity = parse_transfer(tx=tx, mint=mint)
#     if isinstance(transfer_activity, TransferActivity):
#         buyer = transfer_activity.new_authority
#         lamports_transfered = []

#         for index, ix in enumerate(tx.instructions.outer):
#             if (
#                 ix.is_type("transfer")
#                 and ix.is_type("system")
#                 and ix.info["source"] == buyer
#             ):
#                 lamports = ix.info["lamports"]
#                 logger.debug(f"{buyer} paid {lamports}")
#                 lamports_transfered.append(lamports)

#             if not ix.is_parsed:
#                 logger.debug(f"Parsing Inner instruction {index}")
#                 if index not in tx.instructions.inner:
#                     continue

#                 for iix in tx.instructions.inner[index]:
#                     if (
#                         iix.is_type("transfer")
#                         and iix.is_program("system")
#                         and iix.info["source"] == buyer
#                     ):
#                         lamports = iix.info["lamports"]
#                         logger.debug(f"{buyer} paid {lamports}")
#                         lamports_transfered.append(lamports)

#         sale_price = sum(lamports_transfered)
#         logger.debug(f"Calculated price is {sale_price}")
#         if sale_price > 0:
#             return SaleActivity(
#                 transaction_id=tx.transaction_id,
#                 block_time=tx.block_time,
#                 slot=tx.slot,
#                 mint=mint,
#                 new_authority=transfer_activity.new_authority,
#                 old_authority=transfer_activity.old_authority,
#                 new_token_account=transfer_activity.new_token_account,
#                 old_token_account=transfer_activity.old_token_account,
#                 price_lamports=sale_price,
#                 program="unknown",
#             )
#     return None


def parse_sale_mev1(tx: NftTransaction) -> Union[SaleActivity, None]:
    def parse_ix(ix: Instruction) -> Union[SaleActivity, None]:
        marketplace = marketplaces.magic_eden_v1

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.sale.base64_prefix:
            return None
        logger.debug("Is Sale instruction")

        account_indices = marketplace.instructions.sale.account_indices

        old_authority = ix["accounts"][account_indices.old_authority]
        new_authority = ix["accounts"][account_indices.new_authority]
        old_token_account = ix["accounts"][account_indices.old_token_account]

        mint = tx.get_mint_by_accounts(old_authority, new_authority, old_token_account)
        price_lamports = get_me_lamports_price_from_data(ix.data, marketplace.program)

        return SaleActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            old_authority=old_authority,
            new_token_account=old_token_account,
            old_token_account=old_token_account,  # In V1, MagicEden just transfers authority for new token account
            price_lamports=price_lamports,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


def parse_accept_bid_mev1(tx: NftTransaction) -> Union[SaleActivity, None]:
    def parse_ix(ix: Instruction) -> Union[SaleActivity, None]:
        marketplace = marketplaces.magic_eden_v1

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.accept_bid.base64_prefix:
            return None
        logger.debug("Is AcceptBid instruction")

        account_indices = marketplace.instructions.accept_bid.account_indices

        old_authority = ix["accounts"][account_indices.old_authority]
        new_authority = ix["accounts"][account_indices.new_authority]
        old_token_account = ix["accounts"][account_indices.old_token_account]

        mint = tx.get_mint_by_accounts(old_authority, new_authority, old_token_account)
        price_lamports = get_me_lamports_price_from_data(ix.data, marketplace.program)

        return SaleActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            old_authority=old_authority,
            new_token_account=old_token_account,
            old_token_account=old_token_account,  # In V1, MagicEden just transfers authority for new token account
            price_lamports=price_lamports,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


def parse_sale_mev2(tx: NftTransaction) -> Union[SaleActivity, None]:
    def parse_ix(ix: Instruction) -> Union[SaleActivity, None]:
        marketplace = marketplaces.magic_eden_v2

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.sale.base64_prefix:
            return None
        logger.debug("Is Sale instruction")

        account_indices = marketplace.instructions.sale.account_indices

        mint = ix["accounts"][account_indices.mint]
        old_authority = ix["accounts"][account_indices.old_authority]
        new_authority = ix["accounts"][account_indices.new_authority]
        old_token_account = ix["accounts"][account_indices.old_token_account]
        new_token_account = ix["accounts"][account_indices.new_token_account]

        price_lamports = get_me_lamports_price_from_data(ix.data, marketplace.program)

        return SaleActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            old_authority=old_authority,
            new_token_account=new_token_account,
            old_token_account=old_token_account,
            price_lamports=price_lamports,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


# do
def parse_sale_auction_house(tx: NftTransaction) -> Union[SaleActivity, None]:  # noqa
    return None


# do see 3q3VzPrCXfjtXnspPaDb3S9L9wNoMBN9skgXzThDF1KDeaRiYmmtqGJZn2eQCMXMaZ2wAUQxR2Vmpsy6K7jf18gT
def parse_sale_digital_eyes(tx: NftTransaction) -> Union[SaleActivity, None]:  # noqa
    return None


def parse_sale(tx: NftTransaction) -> Union[SaleActivity, None]:
    to_parse = {
        "MagicEdenV1 Sale": parse_sale_mev1,
        "MagicEdenV1 AcceptBid": parse_accept_bid_mev1,
        "MagicEdenV2 Sale": parse_sale_mev2,
        "AuctionHouse": parse_sale_auction_house,
        "DigitalEyes": parse_sale_digital_eyes,
        # "unknown": parse_sale_unknown,
    }

    for marketplace, parser in to_parse.items():
        logger.debug(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx)
        if activity:
            return activity

    return None
