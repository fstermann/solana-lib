from typing import List, Union

from solana.publickey import PublicKey
from solanalib.logger import logger
from solanalib.nft.accounts import AccountInfo
from solanalib.nft.activities import TransferActivity
from solanalib.nft.instructions import InnerInstruction, Instruction, OuterInstruction
from solanalib.nft.transaction import Transaction
from solanalib.rpc.client import Client
from spl.token.instructions import get_associated_token_address


def get_create_instruction_for_account(
    tx: Transaction, account: str, mint: str
) -> Union[OuterInstruction, InnerInstruction, None]:
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
    return None


def get_init_instruction_for_account(
    tx: Transaction, account: str, mint: str
) -> Union[OuterInstruction, InnerInstruction, None]:
    for index, ix in enumerate(tx.instructions.outer):
        if (ix.is_initialize_account_for_mint(mint)) and ix.info["account"] == account:
            return ix

        if index not in tx.instructions.inner:
            continue
        for iix in tx.instructions.inner[index]:
            if (iix.is_initialize_account_for_mint(mint)) and iix.info[
                "account"
            ] == account:
                return iix
    return None


def get_close_instruction_for_account(
    tx: Transaction, account: str
) -> Union[OuterInstruction, InnerInstruction, None]:
    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_close_account(account):
            return ix

        if index not in tx.instructions.inner:
            continue

        for iix in tx.instructions.inner[index]:
            if iix.is_close_account(account):
                return iix
    return None


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


def check_mint(
    mint: str,
    ix: Instruction,
    tx: Transaction,
    new_token_account: str,
    new_authority: str,
):
    logger.debug(
        f"Checking mint for token account {new_token_account} and authority {new_authority}"
    )
    # Mint is specified in the ix
    if ix.info["mint"] == mint:
        return True

    # Search for create ix of the new token account
    create_ix = get_create_instruction_for_account(
        tx=tx, account=new_token_account, mint=mint
    )
    if create_ix:
        return True

    # Search for init ix of the new token account
    init_ix = get_init_instruction_for_account(
        tx=tx, account=new_token_account, mint=mint
    )
    if init_ix:
        return True

    # Check if the pda matches
    if new_authority:
        authority_mint_token_account = str(
            get_associated_token_address(
                owner=PublicKey(new_authority), mint=PublicKey(mint)
            )
        )
        if authority_mint_token_account == new_token_account:
            return True

    # Check if the new_token_account is listed in the post token balance
    post_owners = tx.get_all_post_owners(mint)
    if new_token_account in post_owners:
        logger.debug(
            f"Token account {new_token_account} is owner or has owned the mint"
        )
        return True

    # Get account info from chain and check if mint matches
    client = Client()
    account_info = AccountInfo(client.get_account_info(new_token_account))
    if account_info.has_info:
        if account_info.mint == mint:
            return True

    logger.debug(f"Didn't find correct mint for account {new_token_account}")
    return False


def is_owner_of_account(owner: str, token_account: str, mint: str) -> bool:
    if not owner:
        return False

    pda_token_account = str(
        get_associated_token_address(owner=PublicKey(owner), mint=PublicKey(mint))
    )
    if pda_token_account == token_account:
        return True
    return False


def get_initial_authority_of_token_account(
    new_token_account: str, tx: Transaction, mint: str
):
    # Check for create account ix
    create_ix = get_create_instruction_for_account(
        tx=tx, account=new_token_account, mint=mint
    )
    if create_ix:
        return create_ix.info["wallet"]

    # Check for init account ix
    init_ix = get_init_instruction_for_account(
        tx=tx, account=new_token_account, mint=mint
    )
    if init_ix:
        return init_ix.info["owner"]

    # Check the owners in post_token_balance
    for post_owner in tx.get_all_post_owners(mint):
        if is_owner_of_account(
            owner=post_owner, token_account=new_token_account, mint=mint
        ):
            logger.debug(f"Found new authority by pda {post_owner}")
            return post_owner

    return None


def get_new_authority_of_token_account(
    new_token_account: str, tx: Transaction, mint: str
):
    logger.debug(
        f"[NEW AUTH] Checking new authority for token account {new_token_account}"
    )

    init_authority = get_initial_authority_of_token_account(
        new_token_account=new_token_account, tx=tx, mint=mint
    )
    if not init_authority:
        logger.debug(f"Didn't find authority for token account {new_token_account}")
        return ""

    # Check if another authority is set
    set_authority_ixs = get_setAuthority_instructions_for_account(
        tx=tx, account=new_token_account
    )
    if not set_authority_ixs:
        return init_authority

    new_authority = set_authority_ixs[-1].info["newAuthority"]
    if new_authority:
        logger.debug(f"Changed authority from {init_authority} to {new_authority}")
        return new_authority

    logger.debug(f"Didn't find authority for token account {new_token_account}")
    return ""


def get_old_authority_of_token_account(
    old_token_account: str, transfer_ix: Instruction, tx: Transaction, mint: str
):
    logger.debug(
        f"[OLD AUTH] Checking old authority for token account {old_token_account}"
    )

    # Get simple authority in transfer ix info
    old_authority = transfer_ix.info["authority"]
    if old_authority:
        logger.debug(f"Found old_authority by authority {old_authority}")
        return old_authority

    # Check if closeAccount ix exists
    close_ix = get_close_instruction_for_account(tx, old_token_account)
    if close_ix:
        # The wallet that receives leftover SOL from token account
        old_authority = close_ix.info["destination"]
        logger.debug(f"Found old_authority by close instruction {old_authority}")
        return old_authority

    # Check the owners in post_token_balance
    for pre_owner in tx.get_all_pre_owners(mint):
        if is_owner_of_account(
            owner=pre_owner, token_account=old_token_account, mint=mint
        ):
            logger.debug(f"Found new authority by pda {pre_owner}")
            return pre_owner

    logger.debug(f"Didn't find authority for token account {old_token_account}")
    return ""


def parse_transfer_ix(
    ix: Instruction, tx: Transaction, mint: str
) -> Union[TransferActivity, None]:
    if not ix.is_spl_token_transfer():
        return None

    # Ix is a token transfer
    old_token_account = ix.info["source"]
    new_token_account = ix.info["destination"]

    old_authority = get_old_authority_of_token_account(
        old_token_account=old_token_account, transfer_ix=ix, tx=tx, mint=mint
    )

    # If the new token_account is created in the tx, find the create ix.
    new_authority = get_new_authority_of_token_account(
        new_token_account=new_token_account, tx=tx, mint=mint
    )

    # Check if correct mint is transfered
    if not check_mint(
        mint=mint,
        ix=ix,
        tx=tx,
        new_token_account=new_token_account,
        new_authority=new_authority,
    ):
        return None

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


def parse_transfer_type_transfer(
    tx: Transaction, mint: str
) -> Union[TransferActivity, None]:

    transfers = []

    def parse_inner_ixs(index: int):
        if index not in tx.instructions.inner:
            logger.debug(f"Inner instruction {index} not found")
            return

        for iindex, iix in enumerate(tx.instructions.inner[index]):
            logger.debug(f"Parsing Inner instruction {index}.{iindex}")
            transfer_activity = parse_transfer_ix(ix=iix, tx=tx, mint=mint)
            if transfer_activity:
                transfers.append(transfer_activity)

    for index, ix in enumerate(tx.instructions.outer):
        logger.debug(f"Parsing Outer instruction {index}")

        transfer_activity = parse_transfer_ix(ix=ix, tx=tx, mint=mint)
        if transfer_activity:
            transfers.append(transfer_activity)

        if not ix.is_parsed:
            parse_inner_ixs(index)

    logger.debug(f"Found {len(transfers)} transfers")

    if len(transfers) == 1:
        return transfers[0]
    if len(transfers) > 1:
        # Combine the transfers to include only the first and last accounts
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
    }

    for transfer_type, parser in to_parse.items():
        logger.debug(f"Checking for transfer type {transfer_type}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
