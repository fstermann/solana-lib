from typing import Optional, Union

from pydantic import BaseModel


class AccountIndices(BaseModel):
    mint: Union[int, None]
    new_authority: Union[int, None]
    old_authority: Union[int, None]
    new_token_account: Union[int, None]
    old_token_account: Union[int, None]


class Instruction(BaseModel):
    base64_prefix: str
    hex_prefix: str
    account_indices: AccountIndices


class Instructions(BaseModel):
    delisting: Instruction
    listing: Instruction
    sale: Instruction
    accept_bid: Optional[Instruction]


class Marketplace(BaseModel):
    name: str
    program: str
    authority: str
    instructions: Instructions


class Marketplaces(BaseModel):
    magic_eden_v1: Marketplace
    magic_eden_v2: Marketplace


marketplaces = Marketplaces.parse_file("conf/marketplaces.json")
