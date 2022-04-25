from typing import List, Union

from solanalib.logger import logger
from solanalib.nft.models import (
    Instruction,
    OuterInstruction,
    Transaction,
    TransferActivity,
    AccountInfo,
)
from solanalib.rpc.client import Client
from solanalib.util import SafeDict
from spl.token.instructions import get_associated_token_address
from solana.publickey import PublicKey


def parse_transfer_type_transfer(
    tx: Transaction, mint: str
) -> Union[TransferActivity, None]:
    def get_create_instruction_for_account(
        tx: Transaction, account: str
    ) -> OuterInstruction:
        for index, ix in enumerate(tx.instructions.outer):
            if (ix.is_create_associate_account_for_mint(mint)) and ix.info[
                "account"
            ] == account:
                return ix

            if index not in tx.instructions.inner:
                continue
            for iix in tx.instructions.inner[index]:
                if (iix.is_create_associate_account_for_mint(mint)) and iix.info[
                    "account"
                ] == account:
                    return iix
        return OuterInstruction()

    def get_close_instruction_for_account(
        tx: Transaction, account: str
    ) -> OuterInstruction:
        for index, ix in enumerate(tx.instructions.outer):
            if ix.is_close_account(account):
                return ix

            if index not in tx.instructions.inner:
                continue

            for iix in tx.instructions.inner[index]:
                if iix.is_close_account(account):
                    return iix
        return OuterInstruction()

    def get_init_instruction_for_account(
        tx: Transaction, account: str
    ) -> OuterInstruction:
        for index, ix in enumerate(tx.instructions.outer):
            if (ix.is_initialize_account_for_mint(mint)) and ix.info[
                "account"
            ] == account:
                return ix

            if index not in tx.instructions.inner:
                continue
            for iix in tx.instructions.inner[index]:
                if (iix.is_initialize_account_for_mint(mint)) and iix.info[
                    "account"
                ] == account:
                    return iix
        return OuterInstruction()

    def get_setAuthority_instructions_for_account(
        tx: Transaction, account: str
    ) -> List[Instruction]:
        ixs = []

        for index, ix in enumerate(tx.instructions.outer):
            if ix.is_set_authority_for_account(account):
                ixs.append(ix)

            if index not in tx.instructions.inner:
                continue
            for iix in tx.instructions.inner[index]:
                if iix.is_set_authority_for_account(account):
                    ixs.append(iix)

        return ixs

    def check_mint(ix: Instruction, new_token_account: str, new_authority: str):
        logger.debug(
            f"Checking mint for token account {new_token_account} and authority {new_authority}"
        )
        if ix.info["mint"] == mint:
            return True

        create_ix = get_create_instruction_for_account(tx, new_token_account)
        if create_ix:
            return True

        init_ix = get_init_instruction_for_account(tx, new_token_account)
        if init_ix:
            return True

        if new_authority:
            authority_mint_token_account = str(
                get_associated_token_address(
                    owner=PublicKey(new_authority), mint=PublicKey(mint)
                )
            )
            if authority_mint_token_account == new_token_account:
                return True

        post_owners = tx.get_all_post_owners(mint)
        if new_token_account in post_owners:
            logger.debug(
                f"Token account {new_token_account} is owner or has owned the mint"
            )
            return True

        client = Client()
        account_info = AccountInfo(client.get_account_info(new_token_account))
        if account_info.has_info:
            if account_info.mint == mint:
                return True

        logger.debug(f"Didn't find correct mint for account {new_token_account}")
        return False

    def get_new_authority_of_token_account(new_token_account: str):
        logger.debug(f"Checking new authority for token account {new_token_account}")
        new_authority = None

        create_ix = get_create_instruction_for_account(tx, new_token_account)
        if create_ix:
            new_authority = create_ix.info["wallet"]

        if not new_authority:
            init_ix = get_init_instruction_for_account(tx, new_token_account)
            if init_ix:
                new_authority = init_ix.info["owner"]

        # Check the post_token_balance
        for post_owner in tx.get_all_post_owners(mint):
            if post_owner:
                post_token_account = str(
                    get_associated_token_address(
                        owner=PublicKey(post_owner), mint=PublicKey(mint)
                    )
                )
                if post_token_account == new_token_account:
                    logger.debug(f"Found new authority by pda: {post_owner}")
                    new_authority = post_owner

        if not new_authority:
            logger.debug(f"Didn't find authority for token account {new_token_account}")
            return ""

        # Check if another authority is set
        set_authority_ixs = get_setAuthority_instructions_for_account(
            tx=tx, account=new_token_account
        )
        if not set_authority_ixs:
            return new_authority

        new_authority = set_authority_ixs[-1].info["newAuthority"]
        if new_authority:
            return new_authority

        logger.debug(f"Didn't find authority for token account {new_token_account}")
        return ""

    def get_old_authority_of_token_account(
        old_token_account: str, transfer_ix: Instruction
    ):
        logger.debug(f"Checking old authority for token account {old_token_account}")
        old_authority = transfer_ix.get_authority()
        if old_authority:
            logger.debug(f"Found old_authority by authority {old_authority}")
            return old_authority

        close_ix = get_close_instruction_for_account(tx, old_token_account)
        if close_ix:
            # The wallet that receives leftover SOL from token account
            old_authority = close_ix.info["destination"]
            logger.debug(f"Found old_authority by close instruction {old_authority}")
            return old_authority

        logger.debug(f"Didn't find authority for token account {old_token_account}")
        return ""

    transfers = []

    for index, ix in enumerate(tx.instructions.outer):
        logger.debug(f"Parsing Outer instruction {index}")
        if ix.is_spl_token_transfer():
            # Mint is transfered
            old_token_account = ix.info["source"]
            new_token_account = ix.info["destination"]

            old_authority = get_old_authority_of_token_account(
                old_token_account=old_token_account, transfer_ix=ix
            )

            # If the new token_account is created in the tx, find the create ix.
            new_authority = get_new_authority_of_token_account(
                new_token_account=new_token_account
            )
            logger.debug(f"New authority: {new_authority}")

            # Check if correct mint is transfered
            if not check_mint(
                ix=ix, new_token_account=new_token_account, new_authority=new_authority
            ):
                continue

            transfers.append(
                TransferActivity(
                    transaction_id=tx.transaction_id,
                    block_time=tx.block_time,
                    slot=tx.slot,
                    mint=mint,
                    old_authority=old_authority,
                    new_authority=new_authority,
                    new_token_account=new_token_account,
                    old_token_account=old_token_account,
                )
            )

        if not ix.is_parsed:
            logger.debug(f"Parsing Inner instruction {index}")
            if not index in tx.instructions.inner:
                continue

            for iix in tx.instructions.inner[index]:
                if iix.is_spl_token_transfer():
                    # mint is transfered
                    old_token_account = iix.info["source"]
                    new_token_account = iix.info["destination"]

                    old_authority = get_old_authority_of_token_account(
                        old_token_account=old_token_account, transfer_ix=iix
                    )

                    # If the new token_account is created in the tx, find the create ix.
                    new_authority = get_new_authority_of_token_account(
                        new_token_account=new_token_account,
                    )
                    logger.debug(f"New authority: {new_authority}")

                    # Check if correct mint is transfered
                    if not check_mint(
                        ix=iix,
                        new_token_account=new_token_account,
                        new_authority=new_authority,
                    ):
                        continue

                    transfers.append(
                        TransferActivity(
                            transaction_id=tx.transaction_id,
                            block_time=tx.block_time,
                            slot=tx.slot,
                            mint=mint,
                            old_authority=old_authority,
                            new_authority=new_authority,
                            old_token_account=old_token_account,
                            new_token_account=new_token_account,
                        )
                    )

    logger.debug(f"Found {len(transfers)} transfers")

    if len(transfers) == 1:
        return transfers[0]
    if len(transfers) > 1:
        return TransferActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            old_authority=transfers[0].old_authority,
            new_authority=transfers[-1].new_authority,
            old_token_account=transfers[0].old_token_account,
            new_token_account=transfers[-1].new_token_account,
        )

    return None


def parse_transfer_type_transferChecked(
    tx: Transaction, mint: str
) -> Union[TransferActivity, None]:
    for ix in tx.instructions.outer:
        if ix.is_spl_token_checked_transfer() and ix.info["mint"] == mint:
            # mint is transfered
            old_authority = ix.info["authority"]
            old_token_account = ix.info["source"]
            new_token_account = ix.info["destination"]

            # If the new token_account is created in the tx, find the create ix.
            # create_ix = get_create_instruction_for_account(tx, new_token_account)
            # new_authority = None
            # if create_ix:
            new_authority = tx.get_post_owner(mint)

            return TransferActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                old_authority=old_authority,
                new_authority=new_authority,
                new_token_account=new_token_account,
                old_token_account=old_token_account,
            )
    return None


def parse_transfer(tx: Transaction, mint: str) -> Union[TransferActivity, None]:
    to_parse = {
        "transferChecked": parse_transfer_type_transferChecked,
        "transfer": parse_transfer_type_transfer,
        # "unknown": parse_transfer_type_unknown,
    }

    for transfer_type, parser in to_parse.items():
        logger.info(f"Checking for transfer type {transfer_type}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
