from typing import Union

from solanalib.logger import logger
from solanalib.nft.models import Activity, NFTTransaction, Transaction

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


def _handle_input(
    transaction: Union[dict, Transaction, NFTTransaction], mint: str
) -> Union[str, Transaction]:
    if isinstance(transaction, dict):
        if not mint:
            msg = "Did not receive mint parameter, only got a transaction dictionary."
            logger.error(msg)
            raise AttributeError(msg)
        transaction = NFTTransaction(transaction, mint=mint)

    if isinstance(transaction, NFTTransaction):
        mint = transaction.mint
    elif isinstance(transaction, Transaction):
        if mint is None:
            msg = "Did not receive mint parameter, only got a transaction instance."
            logger.error(msg)
            raise AttributeError(msg)
    else:
        msg = f"Unkown transaction datatype {type(transaction)}"
        logger.error(msg)
        raise AttributeError(msg)

    return transaction, mint


def parse_transaction(
    transaction: Union[dict, Transaction, NFTTransaction], mint: str = None
) -> Activity:
    logger.debug("Checking input")
    transaction, mint = _handle_input(transaction, mint)

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
        activity = parser(transaction, mint)
        if activity:
            return activity

    logger.debug("Unkown Transaction type")
    return None
    # else case
