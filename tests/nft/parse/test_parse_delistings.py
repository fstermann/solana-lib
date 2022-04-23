from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.nft.models import DelistingActivity
from solanalib.nft.parsers.delistings import parse_delisting


class TestParseDelistings:
    def test_parse_delisting_mev1_01(self, load_tx):
        tx = load_tx("delistings", "mev1_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_delisting(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"
        assert activity.old_authority == MagicEdenV1.AUTHORITY
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

    def test_parse_delisting_mev2_01(self, load_tx):
        tx = load_tx("delistings", "mev2_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_delisting(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.old_authority == MagicEdenV2.AUTHORITY
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

    def test_parse_delisting_mev2_02(self, load_tx):
        tx = load_tx("delistings", "mev2_02")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_delisting(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.old_authority == MagicEdenV2.AUTHORITY
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

    def test_parse_delisting_mev2_03(self, load_tx):
        tx = load_tx("delistings", "mev2_03")
        mint = "GMXXVkCnikqj2ngbv12yrypBhN6idL8EV335k55oqXDP"
        activity = parse_delisting(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3YogkYzz6W3gauH8woNKU9Gs7Z6duXR1xBsAWTzdXCdd"
        assert activity.old_authority == MagicEdenV2.AUTHORITY
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
