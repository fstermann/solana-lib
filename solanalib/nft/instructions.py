from typing import Dict, List, Union

from pydantic import BaseModel
from solanalib.logger import logger
from solanalib.util import SafeDict


class Instruction(SafeDict):
    @property
    def parsed(self) -> SafeDict:
        return self["parsed"]

    @property
    def info(self) -> SafeDict:
        return self.parsed["info"]

    @property
    def is_mint_ix(self) -> bool:
        return self.is_type("mintTo") and self.is_program("spl-token")

    def get_authority(self) -> Union[str, None]:
        if "authority" in self.info:
            return self.info["authority"]
        # if "multisigAuthority" in self.info:
        #     return self.info["multisigAuthority"]

        logger.debug("Authority not found in parsed tx")
        return None

    def is_type(self, ttype: str) -> bool:
        return self.parsed["type"] == ttype

    def is_program(self, program: str) -> bool:
        return self["program"] == program

    def is_program_id(self, program_id: str) -> bool:
        return self["programId"] == program_id

    def is_spl_token_transfer(self) -> bool:
        if not (self.is_program("spl-token") and self.parsed["type"] == "transfer"):
            return False
        logger.debug(f"Is program spl-token and type {self.parsed['type']}")

        if not self.info["amount"] == "1":
            return False
        logger.debug("Transferred amount 1")

        return True

    def is_spl_token_checked_transfer(self) -> bool:
        if not (
            self.is_program("spl-token") and self.parsed["type"] == "transferChecked"
        ):
            return False
        logger.debug(f"Is program spl-token and type {self.parsed['type']}")

        if not self.info["tokenAmount"]["amount"] == "1":
            return False
        logger.debug("Transferred amount 1")

        return True

    def is_create_associate_account_for_mint(self, mint: str) -> bool:
        if not (
            self.is_program("spl-associated-token-account") and self.is_type("create")
        ):
            return False
        logger.debug("Is createNewTokenAccount")

        if not self.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_initialize_account_for_mint(self, mint: str) -> bool:
        if not (self.is_program("spl-token") and self.is_type("initializeAccount")):
            return False
        logger.debug("Is initializeAccount")

        if not self.info["mint"] == mint:
            return False
        logger.debug("Is correct mint")

        return True

    def is_close_account(self, account: str) -> bool:
        if not (
            self.is_program("spl-token")
            and self.is_type("closeAccount")
            and self.info["account"] == account
        ):
            return False
        logger.debug("Is close account")

        return True

    def is_set_authority_for_account(self, account: str) -> bool:
        return (
            self.is_type("setAuthority")
            and self.info["authorityType"] == "accountOwner"
            and self.is_program("spl-token")
            and self.info["account"] == account
        )

    @property
    def is_mint_ix(self) -> bool:
        return self.is_type("mintTo") and self.is_program("spl-token")


class OuterInstruction(Instruction):
    @property
    def is_parsed(self) -> bool:
        return "parsed" in self

    @property
    def data(self) -> SafeDict:
        return self["data"]

    def has_data(self) -> bool:
        return "data" in self

    def is_mint(self, mint: str) -> bool:
        return (
            self.is_type("mintTo")
            and self.is_program("spl-token")
            and self.info["mint"] == mint
        )


class InnerInstruction(Instruction):
    @property
    def authority(self) -> SafeDict:
        return self.info["authority"]

    @property
    def new_authority(self) -> SafeDict:
        return self.info["newAuthority"]

    @property
    def source(self) -> SafeDict:
        return self.info["source"]

    def is_create_account_by_program(self, program: str) -> bool:
        return (
            self.is_type("createAccount")
            and self.info["owner"] == program
            and self.is_program("system")
        )

    def is_authority(self, authority: str) -> bool:
        return self.authority == authority

    def is_new_authority(self, new_authority: str) -> bool:
        return self.new_authority == new_authority


class Instructions(BaseModel):
    outer: List[OuterInstruction]
    inner: Dict[int, List[InnerInstruction]]

    def __init__(self, transaction: dict):
        outer_ix = transaction["transaction"]["message"]["instructions"]
        if not outer_ix:
            outer_ix = []

        inner_ix = transaction["meta"]["innerInstructions"]
        if not inner_ix:
            inner_ix = []

        super().__init__(
            outer=[OuterInstruction(ix) for ix in outer_ix],
            inner={
                ix["index"]: [InnerInstruction(iix) for iix in ix["instructions"]]
                for ix in inner_ix
            },
        )
