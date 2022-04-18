from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.nft.models import DelistingActivity, Transaction
from solanalib.logger import logger

# TODO split delist and sales
def parse_delisting_me(
    magic_eden: Union[MagicEdenV1, MagicEdenV2], tx: Transaction, mint: str
) -> Union[DelistingActivity, None]:
    sol_transfered_by = []
    me_authority_transfered = False

    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_program_id(magic_eden.PROGRAM):
            logger.debug(f"Program is {magic_eden.NAME}")
            marketplace = magic_eden.MARKETPLACE

            for iix in tx.instructions.inner[index]:
                if iix.is_type("transfer"):
                    sol_transfered_by.append(iix.source)
                if iix.is_set_authority() and iix.is_authority(magic_eden.AUTHORITY):
                    me_authority_transfered = True
                    new_authority = iix.new_authority

                if ix.has_data():
                    instruction_data = ix.data

    if me_authority_transfered:
        if magic_eden.CANCEL_LISTING_INSTRUCTION in instruction_data:
            logger.debug("Is Cancel Listing tx")
            return DelistingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                marketplace=marketplace,
            )
        logger.debug("ME Authority transfers, but unknown tx")
    return None


def parse_delisting(tx: Transaction, mint: str):
    activity = parse_delisting_me(magic_eden=MagicEdenV1, tx=tx, mint=mint)
    if activity:
        return activity

    activity = parse_delisting_me(magic_eden=MagicEdenV2, tx=tx, mint=mint)
    if activity:
        return activity

    return None
