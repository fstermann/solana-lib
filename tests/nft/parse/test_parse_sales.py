from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.nft.models import SaleActivity
from solanalib.nft.parsers.sales import parse_sale


class TestParseSale:
    def test_parse_sale_mev1(self, load_tx):
        tx = load_tx("sales", "mev1_01")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3H3xcs9xwcqaSJm1EV9Mw9ooKqNCVuYTCntzxhdmuLez"
        assert activity.price_lamports == 1750000000
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

    def test_parse_sale_mev2(self, load_tx):
        pass
        # tx = load_tx("sales", "mev2_01")
        # mint = "Bvn2AsrHX2g2SVH3ByRRhK2qbCDeH1jUmJSWVPzrob5Q"
        # activity = parse_sale(tx=tx, mint=mint)
        # assert isinstance(activity, SaleActivity)
        # assert activity.mint == mint
        # assert activity.new_authority == "BPwzfbHv3JW98kZ3HPJTardvD9pbuD9dVGtoLxiysfk6"
        # assert activity.price_lamports == 3000000000
        # assert activity.marketplace == MagicEdenV2.MARKETPLACE
