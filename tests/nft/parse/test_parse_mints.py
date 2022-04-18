from solanalib.nft.models import MintActivity
from solanalib.nft.parsers.mints import parse_mint


class TestParseMints:
    def test_parse_mint(self, load_tx):
        tx = load_tx("mints", "01")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = parse_mint(tx=tx, mint=mint)
        assert isinstance(activity, MintActivity)
        assert activity.mint == mint
        assert activity.mint_authority == "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"
