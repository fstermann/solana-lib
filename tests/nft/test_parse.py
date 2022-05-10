from solanalib.nft.activities import MintActivity
from solanalib.nft.parse import parse_transaction


class TestParse:
    def test_parse(self, load_tx):
        # The specific parsers are tested in their respective test modules
        tx = load_tx("mints", "01")
        mint_token = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = parse_transaction(transaction=tx)
        assert isinstance(activity, MintActivity)
