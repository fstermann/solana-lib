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
def parse_transaction(
    transaction: Union[dict, Transaction, NFTTransaction], mint: str = None
) -> Activity:
    if isinstance(transaction, dict):
        if not mint:
            msg = "Did not receive mint parameter"
            logger.error(msg)
            raise AttributeError(msg)
        transaction = NFTTransaction(transaction, mint=mint)

    if isinstance(transaction, NFTTransaction):
        mint = transaction.mint

    elif isinstance(transaction, Transaction):
        if mint is None:
            msg = "Did not receive mint parameter"
            logger.error(msg)
            raise AttributeError(msg)
    else:
        msg = f"Unkown transaction datatype {type(transaction)}"
        logger.error(msg)
        raise AttributeError(msg)

    logger.info(f"Parsing transaction {transaction.transaction_id}")

    logger.debug("Check if Transaction is Listing")
    activity = parse_listing(transaction, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Delisting")
    activity = parse_delisting(transaction, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Sale")
    activity = parse_sale(transaction, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Mint")
    activity = parse_mint(transaction, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Transfer")
    activity = parse_transfer(transaction, mint)
    if activity:
        return activity

    logger.debug("Unkown Transaction type")
    return None
    # else case
