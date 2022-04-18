from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.nft.models import ListingActivity
from solanalib.nft.parsers.listings import parse_listing


class TestParseListings:
    def test_parse_listing_mev1(self, load_tx):
        tx = load_tx("listings", "mev1_01")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = parse_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 1750000000
        assert activity.seller == "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

    def test_parse_listing_mev2(self, load_tx):
        tx = load_tx("listings", "mev2_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 7490000000
        assert activity.seller == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
