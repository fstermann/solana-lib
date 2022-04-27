import base58
from solanalib.constants import AuctionHouse, MagicEdenV1, MagicEdenV2


def to_little_endian_from_hex(val):
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()
    str_little = "".join(format(x, "02x") for x in little_hex)
    return str_little


def get_me_lamports_price_from_data(data, program):
    hex_data = base58.b58decode(data).hex()

    program2index = {
        MagicEdenV1.PROGRAM: slice(16, 32),
        MagicEdenV2.PROGRAM: slice(20, 36),
        AuctionHouse.PROGRAM: slice(22, 38),
    }

    if program not in program2index:
        raise NotImplementedError("Unkown program")

    price_hex = hex_data[program2index[program]]

    price_little_endian = to_little_endian_from_hex(price_hex)
    price_lamports = int(price_little_endian, 16)
    return price_lamports
