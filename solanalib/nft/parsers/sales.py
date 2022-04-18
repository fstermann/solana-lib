from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.models import SaleActivity, Transaction

from .util import get_me_listing_price_from_data


def parse_sale_mev1(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    sol_transfered_by = []
    me_authority_transfered = False

    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_program_id(MagicEdenV1.PROGRAM):
            logger.debug(f"Program is {MagicEdenV1.NAME}")
            marketplace = MagicEdenV1.MARKETPLACE

            for iix in tx.instructions.inner[index]:
                if iix.is_type("transfer"):
                    sol_transfered_by.append(iix.source)
                if iix.is_set_authority() and iix.is_authority(MagicEdenV1.AUTHORITY):
                    me_authority_transfered = True
                    new_authority = iix.new_authority

                if ix.has_data():
                    instruction_data = ix.data

    if me_authority_transfered:
        if (sol_transfered_by) and (new_authority in sol_transfered_by):
            logger.debug("Is Sale tx")
            if instruction_data:
                sale_price = get_me_listing_price_from_data(
                    instruction_data, MagicEdenV1.PROGRAM
                )
            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                price_lamports=sale_price,
                marketplace=marketplace,
            )
        logger.debug("ME Authority transfers, but unknown tx")
    return None


def parse_sale_mev2(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    sale_price = None
    new_token_account = None

    for index, ix in enumerate(tx.instructions.outer):
        if ix.is_program_id(MagicEdenV2.PROGRAM):
            logger.debug(f"Program is {MagicEdenV2.NAME}")
            marketplace = MagicEdenV2.MARKETPLACE

            for iix in tx.instructions.inner[index]:
                if (
                    iix.is_type("create")
                    and iix.is_program("spl-associated-token-account")
                    and iix.info["mint"] == mint
                ):
                    logger.debug("Ix created new associate token account")
                    new_token_account = iix.info["account"]

                    if ix.has_data():
                        sale_price = get_me_listing_price_from_data(
                            ix.data, MagicEdenV2.PROGRAM
                        )
                    return SaleActivity(
                        transaction_id=tx.transaction_id,
                        block_time=tx.block_time,
                        slot=tx.slot,
                        mint=mint,
                        new_authority=new_token_account,
                        price_lamports=sale_price,
                        marketplace=marketplace,
                    )
    return None


def parse_sale(tx: Transaction, mint: str):
    activity = parse_sale_mev1(tx=tx, mint=mint)
    if activity:
        return activity

    activity = parse_sale_mev2(tx=tx, mint=mint)
    if activity:
        return activity

    return None


# def check_sale_me_v2(tx: Transaction, mint: str):
#     for index, ix in enumerate(tx.instructions.outer):
#         if ix.is_program_id(MagicEdenV2.PROGRAM):
#             logger.debug(f"Program is {MagicEdenV2.NAME}")
#             marketplace = MagicEdenV2.MARKETPLACE

#             for iix in tx.instructions.inner[index]:
#                 # if iix.is_type("create") and iix.is_program(
#                 #     "spl-associated-token-account"
#                 # ):
#                 #     logger.debug("Create associate token account")
#                 #     if iix.info["mint"] == mint:
#                 #         pass

#                 if iix.is_type("transfer") and iix.is_authority(MagicEdenV2.AUTHORITY):
#                     new_token_account = iix.info["destination"]
#                     if ix.has_data():
#                         instruction_data = ix.data
#                         sale_price = get_me_listing_price_from_data(
#                             instruction_data, MagicEdenV2.PROGRAM
#                         )
#                     return SaleActivity(
#                         transaction_id=tx.transaction_id,
#                         block_time=tx.block_time,
#                         slot=tx.slot,
#                         mint=mint,
#                         new_authority=new_token_account,
#                         price_lamports=sale_price,
#                         marketplace=marketplace,
#                     )
#     return None
