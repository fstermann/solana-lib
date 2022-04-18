from typing import Union
from solanalib.nft.models import Transaction, TransferActivity
from solanalib.logger import logger


# TODO: Define "transfer" and support multiple cases
def parse_transfer(tx: Transaction, mint: str) -> Union[TransferActivity, None]:
    transfered_check = False
    new_token_account = None
    for ix in tx.instructions.outer:
        if ix.is_initialize_account_for_mint(mint):
            new_token_account = ix["parsed"]["info"]["account"]
            logger.debug(f"Found new token account {new_token_account}")

        if ix.is_spl_token_transfer():
            logger.debug("Type is spl-token transfer")
            if (
                ix.info["mint"] == mint
                and ix.info["tokenAmount"]["uiAmountString"] == "1"
            ) or (
                new_token_account
                and new_token_account == ix.info["destination"]
                and ix.info["amount"] == "1"
            ):
                transfered_check = True
                new_authority = ix.info["authority"]
                new_token_account = ix.info["destination"]
                old_token_account = ix.info["source"]

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
