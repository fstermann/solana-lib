from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.nft.models import SaleActivity
from solanalib.nft.parsers.sales import parse_sale


class TestParseSale:
    def test_parse_sale_mev1_01(self, load_tx):
        tx = load_tx("sales", "mev1_01")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "CpkL4HybWzJFqwHWZRR6kZ6SdK2exE1goQhu3Pt3JQFP"
        )
        assert activity.price_lamports == 1750000000
        assert activity.marketplace == MagicEdenV1.MARKETPLACE
        assert activity.new_authority == "3H3xcs9xwcqaSJm1EV9Mw9ooKqNCVuYTCntzxhdmuLez"
        assert activity.old_authority == "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"

    def test_parse_sale_mev1_02(self, load_tx):
        tx = load_tx("sales", "mev1_02")
        mint = "E7QE3BRLpibyf1sdmXz7PziWYDcDdYJJuLoAC66KvG4G"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "8KayTeFzfH29UfujcUwgRu4aSXZGPzWQLwnqqQtTi1PH"
        )
        assert activity.price_lamports == 8880000000
        assert activity.marketplace == MagicEdenV1.MARKETPLACE
        assert activity.new_authority == "DRn7MFrrGPoPiDf8BquppXvZLqDdDkEa62bxZFVyjnh4"
        assert activity.old_authority == "8BnUAvat1qodexeX81NqGNdPSsv9ZPhL3dEtrgHsgekY"

    def test_parse_sale_mev1_03(self, load_tx):
        tx = load_tx("sales", "mev1_03")
        mint = "EqHpPpujGkLM9gsebiDcS4NR9viWjmvoRTdYeB4LvmRX"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "7D5hxWgSRmUohSjgdxbuy793SWKXwhrafCsAJXSx81L1"
        )
        assert activity.price_lamports == 8950000000
        assert activity.marketplace == MagicEdenV1.MARKETPLACE
        assert activity.new_authority == "2BxaLJ7HKgjRE48izSx6o5BBGr5hMn4khvH2Jhv1wVM9"
        assert activity.old_authority == "2LyE4jjMmdU1r1nHkrHuFZ6ND51LZzYWoKN3H8YFzBgA"

    def test_parse_sale_mev2_01(self, load_tx):
        tx = load_tx("sales", "mev2_01")
        mint = "Bvn2AsrHX2g2SVH3ByRRhK2qbCDeH1jUmJSWVPzrob5Q"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "BPwzfbHv3JW98kZ3HPJTardvD9pbuD9dVGtoLxiysfk6"
        )
        assert activity.price_lamports == 3000000000
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
        assert activity.new_authority == "FXA2iPDdHL7cR74vxBb7AgHpqzGFxY9rYXVfqNczZYmF"
        assert activity.old_authority == "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"

    def test_parse_sale_mev2_02(self, load_tx):
        tx = load_tx("sales", "mev2_02")
        mint = "GMXXVkCnikqj2ngbv12yrypBhN6idL8EV335k55oqXDP"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "GDNV3QKvLewWBQif1jpNHCJFYgV3F6GT7ZDD1ruoTkWC"
        )
        assert activity.price_lamports == 17000000000
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
        assert activity.new_authority == "3YogkYzz6W3gauH8woNKU9Gs7Z6duXR1xBsAWTzdXCdd"
        assert activity.old_authority == "7HLjfngPUj5inDWLqc6Bu4vWS6HQx3C2ttvrtRDUAngb"

    def test_parse_sale_mev2_03(self, load_tx):
        tx = load_tx("sales", "mev2_03")
        mint = "DmwPBYvS8D5GSqYtuT2nV51xipqxLo938uYb4NCQjWB7"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "ENdJXpv18wNPiSu7fCkPGHvqM7GRxLdWBBVgzZMbKd7R"
        )
        assert activity.price_lamports == 3500000000
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
        assert activity.new_authority == "7yKzcfvxngQojVc362hRcLNnPXENXFKuVriurvNgw1Jk"
        assert activity.old_authority == "HdwwgWHAvPM2ksceWPCYvXNh5JdfcYdAQgrYkAH426L4"

    def test_parse_sale_mev2_04(self, load_tx):
        tx = load_tx("sales", "mev2_04")
        mint = "FPJtQasfsUmjsJ9pmYVPReNpXMBkVpqavnrcFiWdrx5A"
        activity = parse_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert (
            activity.new_token_account == "J5FMpsTp5Y7ZVtpBbRhB9f3X61iMe3HepKrPyzxvfQ4d"
        )
        assert (
            activity.old_token_account == "HFgFM3jHwN9QLUW9tS7iZhEaR51KmshDw9efkAzHPX85"
        )
        assert activity.price_lamports == 32500000000
        assert activity.marketplace == MagicEdenV2.MARKETPLACE
        assert activity.new_authority == "Fqgd53Bg9GcDAppzcipZfRFr7dEWF7TsqEPNuVwc7u6Y"
        assert activity.old_authority == "2KBxCTCvwQnumQPcXY1Ty414upiQkoPM75hykaRqnzED"
