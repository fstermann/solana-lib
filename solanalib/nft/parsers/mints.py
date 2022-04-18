from typing import Union
from solanalib.nft.models import Transaction, MintActivity
from solanalib.logger import logger

# TODO: Check candy machine
def parse_mint(tx: Transaction, mint: str) -> Union[MintActivity, None]:
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
