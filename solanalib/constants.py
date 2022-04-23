from enum import Enum


class Marketplace(str, Enum):
    MAGIC_EDEN_V1 = "MagicEdenV1"
    MAGIC_EDEN_V2 = "MagicEdenV2"
    AUCTION_HOUSE = "AuctionHouse"


class MagicEdenV1(str, Enum):
    NAME = "MagicEdenV1"
    PROGRAM = "MEisE1HzehtrDpAAT8PnLHjpSSkRYakotTuJRPjTpo8"
    AUTHORITY = "GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp"
    DELISTING_INSTRUCTION = "TE6axTojnp"
    LISTING_INSTRUCTION = "2RD37fomjE"
    SALE_INSTRUCTION = "3UjLyJvuY4"
    MARKETPLACE = Marketplace.MAGIC_EDEN_V1.value


class MagicEdenV2(str, Enum):
    NAME = "MagicEdenV2"
    PROGRAM = "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K"
    AUTHORITY = "1BWutmTvYPwDtmw9abTkS4Ssr8no61spGAvW1X6NDix"
    DELISTING_INSTRUCTION = "ENwHiaH9NA"
    LISTING_INSTRUCTION = "2B3vSpRNKZ"
    SALE_INSTRUCTION = "d6iteQtSVr"
    MARKETPLACE = Marketplace.MAGIC_EDEN_V2.value


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
