from typing import Union

from solanalib.logger import logger
from solanalib.nft.activities import DelistingActivity
from solanalib.nft.instructions import Instruction
from solanalib.nft.marketplaces import marketplaces
from solanalib.nft.nft_transaction import NftTransaction


def parse_delisting_mev1(tx: NftTransaction) -> Union[DelistingActivity, None]:
    def parse_ix(ix: Instruction) -> Union[DelistingActivity, None]:
        marketplace = marketplaces.magic_eden_v1

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.delisting.base64_prefix:
            return None
        logger.debug("Is Delisting instruction")

        account_indices = marketplace.instructions.delisting.account_indices

        old_authority = marketplace.authority
        new_authority = ix["accounts"][account_indices.new_authority]
        old_token_account = ix["accounts"][account_indices.old_token_account]

        mint = tx.get_mint_by_accounts(old_authority, new_authority, old_token_account)

        return DelistingActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            old_authority=old_authority,
            new_authority=new_authority,
            old_token_account=old_token_account,
            new_token_account=old_token_account,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


def parse_delisting_mev2(tx: NftTransaction) -> Union[DelistingActivity, None]:
    def parse_ix(ix: Instruction) -> Union[DelistingActivity, None]:
        marketplace = marketplaces.magic_eden_v2

        if not ix.is_program_id(marketplace.program):
            return None
        logger.debug(f"Program is {marketplace.name}")

        if not ix.data[0:10] == marketplace.instructions.delisting.base64_prefix:
            return None
        logger.debug("Is Delisting instruction")

        account_indices = marketplace.instructions.delisting.account_indices

        old_authority = marketplace.authority
        new_authority = ix["accounts"][account_indices.new_authority]
        old_token_account = ix["accounts"][account_indices.old_token_account]

        mint = ix["accounts"][account_indices.mint]

        return DelistingActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            old_authority=old_authority,
            new_authority=new_authority,
            old_token_account=old_token_account,
            new_token_account=old_token_account,
            program=marketplace.name,
        )

    return tx.parse_ixs(parse_ix)


def parse_delisting(tx: NftTransaction):
    to_parse = {
        "MagicEdenV1": parse_delisting_mev1,
        "MagicEdenV2": parse_delisting_mev2,
    }

    for marketplace, parser in to_parse.items():
        logger.debug(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx)
        if activity:
            return activity

    return None
