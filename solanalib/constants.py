from enum import Enum


class Marketplace(str, Enum):
    MAGIC_EDEN_V1 = "MagicEdenV1"
    MAGIC_EDEN_V2 = "MagicEdenV2"


class MagicEden(str, Enum):
    PROGRAM_V1 = "MEisE1HzehtrDpAAT8PnLHjpSSkRYakotTuJRPjTpo8"
    PROGRAM_V2 = "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K"
    AUTHORITY_V1 = "GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp"
    AUTHORITY_V2 = "1BWutmTvYPwDtmw9abTkS4Ssr8no61spGAvW1X6NDix"
    CANCEL_LISTING_INSTRUCTION = "TE6axTojnpk"


class Metaplex(str, Enum):
    METADATA_PROGRAM = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    CANDY_MACHINE_V2 = "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ"


class Token(str, Enum):
    PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    ASSOCIATE_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
