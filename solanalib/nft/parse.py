import base58
from solanalib.constants import MagicEden
from solanalib.logger import logger
from solanalib.nft.models import (
    Activity,
    DelistingActivity,
    ListingActivity,
    MintActivity,
    SaleActivity,
    Transaction,
    TransferActivity,
)
import numpy as np
import struct

# Transaction types to check
# - Listing
# - Cancel Listing or Sale
# - Mint
# - Transfer
def parse_transaction(transaction: dict, mint: str) -> Activity:
    logger.debug("Check if Transaction is Listing")

    tx = Transaction(transaction)

    activity = check_listing(tx, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Delisting or Sale")
    activity = check_delisting_or_sale(tx, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Mint")
    activity = check_mint(tx, mint)
    if activity:
        return activity

    logger.debug("Check if Transaction is Transfer")
    activity = check_transfer(tx, mint)
    if activity:
        return activity

    logger.debug("Unkown Transaction type")
    return None
    # else case


def check_listing(tx: Transaction, mint: str):
    me_program_check = False
    me_authority_check = False

    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_program_id(MagicEden.PROGRAM_V1):
            logger.debug("Is MagicEdenV1")

            for iix in tx.instructions.inner[index]:
                if iix.is_create_account_by_program(MagicEden.PROGRAM_V1):
                    me_program_check = True
                if iix.is_set_authority() and iix.is_new_authority(MagicEden.AUTHORITY):
                    me_authority_check = True
                    listing_authority = iix.authority
                    if ix.has_data():
                        listing_price = get_me_listing_price_from_data(ix.data)

    if me_program_check & me_authority_check:
        logger.debug("Is listing tx")
        return ListingActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            listing_authority=listing_authority,
            price_lamports=listing_price,
        )
    return None


def to_little_endian_from_hex(val):
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()
    str_little = "".join(format(x, "02x") for x in little_hex)
    return str_little


def get_me_listing_price_from_data(data):
    price_hex = base58.b58decode(data).hex()[16:24]
    price_little_endian = to_little_endian_from_hex(price_hex)
    price_lamports = int(price_little_endian, 16)
    return price_lamports


def check_delisting_or_sale(tx: Transaction, mint: str):
    sol_transfered_by = []
    me_authority_transfered = False

    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_program_id(MagicEden.PROGRAM_V1):
            logger.debug("Is MagicEdenV1")

            for iix in tx.instructions.inner[index]:
                if iix.is_type("transfer"):
                    sol_transfered_by.append(iix.source)
                if iix.is_set_authority() and iix.is_authority(MagicEden.AUTHORITY):
                    me_authority_transfered = True
                    new_authority = iix.new_authority

                if ix.has_data():
                    instruction_data = ix.data

    if me_authority_transfered:
        if MagicEden.CANCEL_LISTING_INSTRUCTION == instruction_data:
            logger.debug("Is Cancel Listing tx")
            return DelistingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
            )
        if (sol_transfered_by) and (new_authority in sol_transfered_by):
            logger.debug("Is Sale tx")
            if instruction_data:
                sale_price = get_me_listing_price_from_data(instruction_data)
            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                price_lamports=sale_price,
            )
        logger.debug("ME Authority transfers, but unknown tx")
    return None


def check_mint(tx: Transaction, mint: str):
    for ix in tx.instructions.outer:
        if ix.is_mint(mint):
            logger.debug("Is correct mint tx")
            return MintActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                mint_authority=ix.info["mintAuthority"],
            )
    return None
    # if Metaplex.CANDY_MACHINE_V2 in program_ids:
    #     return True


def check_transfer(tx: Transaction, mint: str):
    transfered_check = False
    new_token_account = None
    for ix in tx.instructions.outer:
        if (
            ix["parsed"]["type"] == "initializeAccount"
            and ix["program"] == "spl-token"
            and ix["parsed"]["info"]["mint"] == mint
        ):
            new_token_account = ix["parsed"]["info"]["account"]
            logger.debug(f"Found new token account {new_token_account}")

        if (
            ix["parsed"]["type"] in ["transferChecked", "transfer"]
            and ix["program"] == "spl-token"
        ):
            logger.debug("Type is spl-token transfer")
            if (
                ix["parsed"]["info"]["mint"] == mint
                and ix["parsed"]["info"]["tokenAmount"]["uiAmountString"] == "1"
            ) or (
                new_token_account
                and new_token_account == ix["parsed"]["info"]["destination"]
                and ix["parsed"]["info"]["amount"] == "1"
            ):
                transfered_check = True
                new_authority = ix["parsed"]["info"]["authority"]
                new_token_account = ix["parsed"]["info"]["destination"]
                old_token_account = ix["parsed"]["info"]["source"]

    if transfered_check:
        logger.debug("Is transfer tx")
        return TransferActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            new_token_account=new_token_account,
            old_token_account=old_token_account,
        )
    return None
