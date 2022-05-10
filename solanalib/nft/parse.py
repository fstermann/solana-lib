from solanalib.logger import logger
from solanalib.nft.activities import Activity, UnknownActivity
from solanalib.nft.nft_transaction import NftTransaction

from .parsers.delistings import parse_delisting
from .parsers.listings import parse_listing
from .parsers.mints import parse_mint
from .parsers.sales import parse_sale
from .parsers.transfers import parse_transfer

# Transaction types to check
# - Listing
# - Cancel Listing or Sale
# - Mint
# - Transfer


def parse_transaction(transaction: NftTransaction) -> Activity:
    logger.info(f"Parsing transaction {transaction.transaction_id}")

    to_check = {
        "Listing": parse_listing,
        "Delisting": parse_delisting,
        "Sale": parse_sale,
        "Mint": parse_mint,
        "Transfer": parse_transfer,
    }
    for activity_type, parser in to_check.items():
        logger.debug(f"Check if transaction is '{activity_type}'")
        activity = parser(transaction)
        if activity:
            return activity

    logger.debug("Unkown Transaction type")
    return UnknownActivity(
        transaction_id=transaction.transaction_id,
        block_time=transaction.block_time,
        slot=transaction.slot,
    )
