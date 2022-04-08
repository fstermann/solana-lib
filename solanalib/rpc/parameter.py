from enum import Enum


class Encoding(Enum):
    JSON = "json"
    JSON_PARSED = "jsonParsed"
    BASE_58 = "base58"  # slow
    BASE_64 = "base64"


class Commitment(Enum):
    FINALIZED = "finalized"
