from typing import Union

from solanalib.constants import Metaplex
from solanalib.logger import logger
from solanalib.nft.activities import MintActivity
from solanalib.nft.instructions import Instruction
from solanalib.nft.nft_transaction import NftTransaction


def parse_mint_other(tx: NftTransaction) -> Union[MintActivity, None]:
    def parse_ix(ix: Instruction):
        if not ix.is_mint_ix:
            return None
        logger.debug("Is mint ix")

        mint = ix.info["mint"]
        new_authority = ix.info["mintAuthority"]
        new_token_account = ix.info["account"]
        program = ix["program"]

        return MintActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            new_token_account=new_token_account,
            program=program,
        )

    return tx.parse_ixs(parse_ix)


def parse_mint_candy_machine_v1(tx: NftTransaction) -> Union[MintActivity, None]:
    def parse_ix(ix: Instruction):
        if not ix.is_mint_ix:
            return None
        logger.debug("Is mint ix")

        if Metaplex.CANDY_MACHINE_V1 not in tx.account_keys:
            return None
        logger.debug("Program is CandyMachineV1")

        mint = ix.info["mint"]
        new_authority = ix.info["mintAuthority"]
        new_token_account = ix.info["account"]

        return MintActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            new_token_account=new_token_account,
            program="CandyMachineV1",
        )

    return tx.parse_ixs(parse_ix)


def parse_mint_candy_machine_v2(tx: NftTransaction) -> Union[MintActivity, None]:
    def parse_ix(ix: Instruction):
        if not ix.is_mint_ix:
            return None
        logger.debug("Is mint ix")

        if Metaplex.CANDY_MACHINE_V2 not in tx.account_keys:
            return None
        logger.debug("Program is CandyMachineV2")

        mint = ix.info["mint"]
        new_authority = ix.info["mintAuthority"]
        new_token_account = ix.info["account"]

        return MintActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            new_token_account=new_token_account,
            program="CandyMachineV2",
        )

    return tx.parse_ixs(parse_ix)


def parse_mint(tx: NftTransaction) -> Union[MintActivity, None]:
    to_parse = {
        "CandyMachineV1": parse_mint_candy_machine_v1,
        "CandyMachineV2": parse_mint_candy_machine_v2,
        "OtherMint": parse_mint_other,
    }

    for marketplace, parser in to_parse.items():
        logger.debug(f"Checking mint-program {marketplace}")
        activity = parser(tx=tx)
        if activity:
            return activity

    return None
