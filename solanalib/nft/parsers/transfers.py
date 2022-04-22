from typing import Union

from solanalib.logger import logger
from solanalib.nft.models import (
    InnerInstruction,
    OuterInstruction,
    Transaction,
    TransferActivity,
)


def parse_transfer_type_transfer(
    tx: Transaction, mint: str
) -> Union[TransferActivity, None]:
    """
    Need to check for two instructions:
    1)  create or initializeAccount
        -> create new token account for the mint
    2)  transfer
        -> transfer to new token account

    """

    def is_create(ix: OuterInstruction) -> bool:
        if not (ix.is_program("spl-associated-token-account") and ix.is_type("create")):
            return False
        logger.debug("Is createNewTokenAccount")

        if not ix.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_initializeAccount(ix: OuterInstruction) -> bool:
        if not (ix.is_program("spl-token") and ix.is_type("initializeAccount")):
            return False
        logger.debug("Is initializeAccount")

        if not ix.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_transfer(ix: OuterInstruction) -> bool:
        if not (ix.is_program("spl-token") and ix.is_type("transfer")):
            return False
        logger.debug("Is transfer")

        return True

    is_create_flag = False
    is_transfer_flag = False
    new_authority = None
    old_token_account = None
    new_token_account = None

    for ix in tx.instructions.outer:
        if is_create(ix) or is_initializeAccount(ix):
            is_create_flag = True

        if is_transfer(ix):
            is_transfer_flag = True
            new_authority = ix.info["authority"]  # new owner
            old_token_account = ix.info["source"]
            new_token_account = ix.info["destination"]

        if is_create_flag and is_transfer_flag:
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


def parse_transfer_type_transferChecked(
    tx: Transaction, mint: str
) -> Union[TransferActivity, None]:
    for ix in tx.instructions.outer:
        if not (ix.is_program("spl-token") and ix.is_type("transferChecked")):
            continue
        logger.debug("Is transferChecked")

        if not ix.info["mint"] == mint:
            continue
        logger.debug("Is correct mint")

        new_authority = ix.info["authority"]  # new owner
        old_token_account = ix.info["source"]
        new_token_account = ix.info["destination"]

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


def parse_transfer_type_unknown(
    tx: Transaction, mint: str
) -> Union[TransferActivity, None]:
    """
    Need to check for two instructions:
    1)  create or initializeAccount
        -> create new token account for the mint
    2)  transfer
        -> transfer to new token account

    """

    def is_create(ix: InnerInstruction) -> bool:
        if not (ix.is_program("spl-associated-token-account") and ix.is_type("create")):
            return False
        logger.debug("Is createNewTokenAccount")

        if not ix.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_initializeAccount(ix: InnerInstruction) -> bool:
        if not (ix.is_program("spl-token") and ix.is_type("initializeAccount")):
            return False
        logger.debug("Is initializeAccount")

        if not ix.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_transfer(ix: InnerInstruction) -> bool:
        if not (ix.is_program("spl-token") and ix.is_type("transfer")):
            return False
        logger.debug("Is transfer")

        return True

    is_create_flag = False
    is_transfer_flag = False
    new_authority = None
    old_token_account = None
    new_token_account = None

    for index, ix in enumerate(tx.instructions.outer):
        if not index in tx.instructions.inner:
            continue

        for iix in tx.instructions.inner[index]:
            if is_create(iix) or is_initializeAccount(iix):
                new_authority = iix.info["owner"]  # new owner
                is_create_flag = True

            if is_transfer(iix):
                is_transfer_flag = True
                # new_authority = iix.info["authority"]  # new owner
                old_token_account = iix.info["source"]
                new_token_account = iix.info["destination"]

    if is_create_flag and is_transfer_flag:
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


def parse_transfer(tx: Transaction, mint: str) -> Union[TransferActivity, None]:
    to_parse = {
        "transferChecked": parse_transfer_type_transferChecked,
        "transfer": parse_transfer_type_transfer,
        "unknown": parse_transfer_type_unknown,
    }

    for transfer_type, parser in to_parse.items():
        logger.info(f"Checking for transfer type {transfer_type}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
