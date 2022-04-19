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

        tx = load_tx("listings", "mev1_02")
        mint = "EqHpPpujGkLM9gsebiDcS4NR9viWjmvoRTdYeB4LvmRX"
        activity = parse_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 8950000000
        assert activity.seller == "2LyE4jjMmdU1r1nHkrHuFZ6ND51LZzYWoKN3H8YFzBgA"
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

        tx = load_tx("listings", "mev1_03")
        mint = "FPJtQasfsUmjsJ9pmYVPReNpXMBkVpqavnrcFiWdrx5A"
        activity = parse_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 6500000000
        assert activity.seller == "BcKiawEXhLHwC4T1yPwSGRTzgHQdPa9TmCGuYpnaVMk9"
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

        tx = load_tx("listings", "mev2_02")
        mint = "Gnbzi1PnMNS1n35ByDTx37ZsbY5R4ac1HMMrfjgKupu5"
        activity = parse_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 187690000000
        assert activity.seller == "8puHvsobwPa7taCVknWcFyaDDYjNAGvLHUEmZ33Ye8vs"
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

        tx = load_tx("listings", "mev2_03")
        mint = "8ychX3Su5pXbDspTwLkN7NzP4RQ1C8q9xYCRJP1NKAyA"
        activity = parse_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 29990000000
        assert activity.seller == "BP9a7nk1GJFAeLDJL1BxnXDRxzJviHT66w6Qcznz3t1X"
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
