from enum import Enum


class Marketplace(str, Enum):
    MAGIC_EDEN_V1 = "MagicEden V1"
    MAGIC_EDEN_V2 = "MagicEden V2"
    AUCTION_HOUSE = "AuctionHouse"


class AuctionHouse(str, Enum):
    NAME = "AuctionHouse"
    PROGRAM = "hausS13jsjafwWwGqZTUQRmWyvyxn9EQpqMwV1PBBmk"
    LISTING_INSTRUCTION = "81r6u24fHZ"
    MARKETPLACE = Marketplace.AUCTION_HOUSE.value


class Metaplex(str, Enum):
    METADATA_PROGRAM = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    CANDY_MACHINE_V1 = "cndyAnrLdpjq1Ssp1z8xxDsB8dxe7u4HL5Nxi2K5WXZ"
    CANDY_MACHINE_V2 = "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ"


class Token(str, Enum):
    PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    ASSOCIATE_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
