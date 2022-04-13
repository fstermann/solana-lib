import json
from solanalib.constants import MagicEdenV1, MagicEdenV2, Marketplace

from solanalib.nft.models import (
    DelistingActivity,
    ListingActivity,
    MintActivity,
    SaleActivity,
    Transaction,
    TransferActivity,
)
from solanalib.nft.parse import (
    check_delisting_or_sale,
    check_listing,
    check_mint,
    check_transfer,
)


class TestParse:
    def load_example_tx(self, file_name: str) -> Transaction:
        with open(f"tests/nft/txs/{file_name}.json", "r") as f:
            data = json.load(f)
        tx = Transaction(transaction=data["result"])
        return tx

    def test_parse_listing_mev1(self):
        tx = self.load_example_tx("tx_listing_mev1")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = check_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 1750000000
        assert (
            activity.listing_authority == "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"
        )
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

    def test_parse_listing_mev2(self):
        tx = self.load_example_tx("tx_listing_mev2")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = check_listing(tx=tx, mint=mint)
        assert isinstance(activity, ListingActivity)
        assert activity.mint == mint
        assert activity.price_lamports == 7490000000
        assert (
            activity.listing_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        )
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

    def test_parse_delisting_mev1(self):
        tx = self.load_example_tx("tx_delisting_mev1")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = check_delisting_or_sale(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

    def test_parse_delisting_mev2(self):
        tx = self.load_example_tx("tx_delisting_mev2")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = check_delisting_or_sale(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

        tx = self.load_example_tx("tx_delisting2_mev2")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = check_delisting_or_sale(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

        tx = self.load_example_tx("tx_delisting3_mev2")
        mint = "GMXXVkCnikqj2ngbv12yrypBhN6idL8EV335k55oqXDP"
        activity = check_delisting_or_sale(tx=tx, mint=mint)
        assert isinstance(activity, DelistingActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3YogkYzz6W3gauH8woNKU9Gs7Z6duXR1xBsAWTzdXCdd"
        assert activity.marketplace == MagicEdenV2.MARKETPLACE

    def test_parse_mint_mev1(self):
        tx = self.load_example_tx("tx_mint_mev1")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = check_mint(tx=tx, mint=mint)
        assert isinstance(activity, MintActivity)
        assert activity.mint == mint
        assert activity.mint_authority == "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"

    def test_parse_sale_mev1(self):
        tx = self.load_example_tx("tx_sale_mev1")
        mint = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = check_delisting_or_sale(tx=tx, mint=mint)
        assert isinstance(activity, SaleActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3H3xcs9xwcqaSJm1EV9Mw9ooKqNCVuYTCntzxhdmuLez"
        assert activity.price_lamports == 1750000000
        assert activity.marketplace == MagicEdenV1.MARKETPLACE

    def test_parse_transfer_v1(self):
        tx = self.load_example_tx("tx_transfer_v1")
        mint = "2cQaPyqMaRhU4d9kASVtehNnBYekisjVVf3oTKao3K9E"
        activity = check_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3Z9zoXZPS4NnFkzrMAY6a5KdzfMcRPkrtmNJbtWz2wFU"
        assert (
            activity.new_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )
        assert (
            activity.old_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )

        tx = self.load_example_tx("tx_transfer2_v1")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = check_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "CXx7CiK43NbhdthMZXA6wC9JPbraLjvZcRwTWuRsLkwH"
        assert (
            activity.new_token_account == "7mTZW2DrvEXcPq5XaT4wRvbqX51CkkNVuA3K8cARy5sx"
        )
        assert (
            activity.old_token_account == "HN5EzbsER7fud5QxhcHXYS8ddVAJgxzoRwMbQJBytbnE"
        )

    #     tx = self.load_example_tx("tx_transfer2")
    #     mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
    #     activity = check_transfer(tx=tx, mint=mint)
    #     assert isinstance(activity, TransferActivity)
    #     assert activity.mint == mint

    #     tx = self.load_example_tx("tx_transfer3")
    #     mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
    #     activity = check_transfer(tx=tx, mint=mint)
    #     assert isinstance(activity, TransferActivity)
    #     assert activity.mint == mint
