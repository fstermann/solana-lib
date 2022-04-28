from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.activities import DelistingActivity
from solanalib.nft.transaction import Transaction


def parse_delisting_mev1(tx: Transaction, mint: str) -> Union[DelistingActivity, None]:
    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV1.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV1.NAME}")
        marketplace = MagicEdenV1.MARKETPLACE

        if ix.data[0:10] == MagicEdenV1.DELISTING_INSTRUCTION:
            logger.debug("Is Delisting instruction")
            new_authority = ix["accounts"][0]  # 1st account
            old_authority = MagicEdenV1.AUTHORITY
            old_token_account = ix["accounts"][1]

            return DelistingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                old_authority=old_authority,
                new_authority=new_authority,
                old_token_account=old_token_account,
                new_token_account=old_token_account,
                program=marketplace,
            )
    return None


def parse_delisting_mev2(tx: Transaction, mint: str) -> Union[DelistingActivity, None]:
    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV2.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV2.NAME}")
        marketplace = MagicEdenV2.MARKETPLACE

        if ix.data[0:10] == MagicEdenV2.DELISTING_INSTRUCTION:
            logger.debug("Is Delisting Instruction")
            if ix["accounts"][3] != mint:  # 4th account
                logger.debug("Mint did not match")

            new_authority = ix["accounts"][0]  # 1st account
            old_authority = MagicEdenV2.AUTHORITY
            old_token_account = ix["accounts"][2]

            return DelistingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                old_authority=old_authority,
                new_authority=new_authority,
                old_token_account=old_token_account,
                new_token_account=old_token_account,
                program=marketplace,
            )
    return None


def parse_delisting(tx: Transaction, mint: str):
    to_parse = {
        "MagiEdenV1": parse_delisting_mev1,
        "MagiEdenV2": parse_delisting_mev2,
    }

    for marketplace, parser in to_parse.items():
        logger.info(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
