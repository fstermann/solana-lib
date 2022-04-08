from solanalib.logger import logger
from solanalib.nft.models import (
    Transaction,
    Activity,
    MintActivity,
    SaleActivity,
    ListingActivity,
    TransferActivity,
    CancelListingActivity,
)
from solanalib.constants import MagicEden


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
        if ix["programId"] == MagicEden.PROGRAM_V1:
            logger.debug("Is MagicEdenV1")
            for iix in tx.instructions.inner[index]:
                if (
                    (iix["parsed"]["type"] == "createAccount")
                    & (iix["parsed"]["info"]["owner"] == MagicEden.PROGRAM_V1)
                    & (iix["program"] == "system")
                ):
                    me_program_check = True
                if (
                    (iix["parsed"]["type"] == "setAuthority")
                    & (iix["parsed"]["info"]["authorityType"] == "accountOwner")
                    & (iix["parsed"]["info"]["newAuthority"] == MagicEden.AUTHORITY)
                    & (iix["program"] == "spl-token")
                ):
                    me_authority_check = True
                    listing_authority = iix["parsed"]["info"]["authority"]
                    if "data" in ix:
                        listing_price = get_me_listing_price_from_data(ix["data"])

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


def get_me_listing_price_from_data(data):
    # const priceHex = bs58
    #     .decode(instructionData)
    #     .toString("hex")
    #     .substring(16, 34);
    # // console.log("Decode Instruction Data:", priceHex);
    # const sol =
    #     parseInt(Buffer.from(priceHex, "hex").readUIntLE(0, 8).toString(), 10) /
    #     LAMPORTS_PER_SOL;
    # // console.log("Instruction Data Price:", sol);
    # return sol;
    return 0


def check_delisting_or_sale(tx: Transaction, mint: str):
    sol_transfered_by = []
    me_authority_transfered = False

    for index, ix in enumerate(tx.instructions.outer):
        if ix["programId"] == MagicEden.PROGRAM_V1:
            logger.debug("Is MagicEdenV1")
            for iix in tx.instructions.inner[index]:
                if iix["parsed"]["type"] == "transfer":
                    sol_transfered_by.append(iix["parsed"]["info"]["source"])

                if (
                    (iix["parsed"]["type"] == "setAuthority")
                    & (iix["parsed"]["info"]["authorityType"] == "accountOwner")
                    & (iix["parsed"]["info"]["authority"] == MagicEden.AUTHORITY)
                    & (iix["program"] == "spl-token")
                ):
                    me_authority_transfered = True
                    new_authority = iix["parsed"]["info"]["newAuthority"]

                if "data" in ix:
                    instruction_data = ix["data"]

    if me_authority_transfered:
        if MagicEden.CANCEL_LISTING_INSTRUCTION == instruction_data:
            logger.debug("Is Cancel Listing tx")
            return CancelListingActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
            )
        if (sol_transfered_by) & (new_authority in sol_transfered_by):
            logger.debug("Is Sale tx")
            if instruction_data:
                sale_price = get_me_listing_price_from_data(instruction_data)
            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                sale_price=sale_price,
            )
        logger.debug("ME Authority transfers, but unknown tx")
    return None


def check_mint(tx: Transaction, mint: str):
    for ix in tx.instructions.outer:
        if ix["parsed"]["type"] == "mintTo":
            logger.debug("Has mintTo")
            logger.debug(f"Mint in tx {ix['parsed']['mint']}")
            logger.debug(f"Target mint {mint}")
            logger.debug(ix["parsed"])
            if ix["parsed"]["info"]["mint"] == mint:
                logger.debug("Is mint tx")
                return MintActivity(
                    transaction_id=tx.transaction_id,
                    block_time=tx.block_time,
                    slot=tx.slot,
                    mint=mint,
                    mint_authority=ix["parsed"]["mintAuthority"],
                )
    return None
    # if Metaplex.CANDY_MACHINE_V2 in program_ids:
    #     return True


def check_transfer(tx: Transaction, mint: str):
    transfered_check = False
    for ix in tx.instructions.outer:
        if (
            (ix["parsed"]["type"] == "initializeAccount")
            & (ix["program"] == "spl-token")
            & (ix["parsed"]["info"]["mint"] == mint)
        ):
            new_token_account = ix["parsed"]["info"]["account"]

        if (ix["parsed"]["type"] in ["transferChecked", "transfer"]) & (
            ix["program"] == "spl-token"
        ):
            if (ix["parsed"]["info"]["mint"] == mint) & (
                ix["parsed"]["info"]["tokenAmount"]["uiAmountString"] == "1"
            ) or (
                new_token_account & new_token_account
                == ix["parsed"]["info"]["destination"] & ix["parsed"]["info"]["amount"]
                == "1"
            ):
                transfered_check = True
                new_authority = ix["parsed"]["info"]["authority"]
                source_token_account = ix["parsed"]["info"]["source"]

    if transfered_check:
        logger.debug("Is transfer tx")
        return TransferActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            transfered_from_account=source_token_account,
        )
    return None
