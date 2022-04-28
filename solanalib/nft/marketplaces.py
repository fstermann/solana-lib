from typing import Dict, Union

from pydantic import BaseModel


class AccountIndices(BaseModel):
    mint: Union[int, None]
    new_authority: int
    old_authority: int
    new_token_account: int
    old_token_account: int


class Instruction(BaseModel):
    base64_prefix: str
    hex_prefix: str
    account_indices: AccountIndices


class Instructions(BaseModel):
    delisting: Instruction
    listing: Instruction
    sale: Instruction


class Marketplace(BaseModel):
    name: str
    program: str
    authority: str
    instructions: Instructions


class Marketplaces(BaseModel):
    magic_eden_v1: Marketplace
    magic_eden_v2: Marketplace


marketplaces = Marketplaces.parse_file("conf/marketplaces.json")

print(marketplaces)
