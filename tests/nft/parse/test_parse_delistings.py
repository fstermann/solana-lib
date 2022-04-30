from solanalib.nft.activities import DelistingActivity
from solanalib.nft.marketplaces import marketplaces
from solanalib.nft.parsers.delistings import parse_delisting


class TestParseDelistings:
    def test_parse_delisting_mev1_01(self, load_tx):
        tx = load_tx("delistings", "mev1_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_delisting(tx=tx)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"
        assert activity.old_authority == marketplaces.magic_eden_v1.authority
        assert activity.program == marketplaces.magic_eden_v1.name

    def test_parse_delisting_mev2_01(self, load_tx):
        tx = load_tx("delistings", "mev2_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_delisting(tx=tx)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.old_authority == marketplaces.magic_eden_v2.authority
        assert activity.program == marketplaces.magic_eden_v2.name

    def test_parse_delisting_mev2_02(self, load_tx):
        tx = load_tx("delistings", "mev2_02")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_delisting(tx=tx)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.old_authority == marketplaces.magic_eden_v2.authority
        assert activity.program == marketplaces.magic_eden_v2.name

    def test_parse_delisting_mev2_03(self, load_tx):
        tx = load_tx("delistings", "mev2_03")
        mint = "GMXXVkCnikqj2ngbv12yrypBhN6idL8EV335k55oqXDP"
        activity = parse_delisting(tx=tx)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3YogkYzz6W3gauH8woNKU9Gs7Z6duXR1xBsAWTzdXCdd"
        assert activity.old_authority == marketplaces.magic_eden_v2.authority
        assert activity.program == marketplaces.magic_eden_v2.name
