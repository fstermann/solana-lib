from solanalib.nft.parsers.transfers import parse_transfer
from solanalib.nft.models import TransferActivity


class TestParseTransfers:
    def test_parse_transfer_transferChecked_01(self, load_tx):
        tx = load_tx("transfers", "v0_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"
        assert (
            activity.new_token_account == "BEPURPfP9LbAypFaDVVEf9KzXAoVmFA9SahdqcVJPvB"
        )
        assert (
            activity.old_token_account == "DbM2nNjaPWJ5NfxYt68QZR2DAtEuXfyA282A5RE6ZXk4"
        )

    def test_parse_transfer_transferChecked_02(self, load_tx):
        tx = load_tx("transfers", "v0_02")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"
        assert (
            activity.new_token_account == "BEPURPfP9LbAypFaDVVEf9KzXAoVmFA9SahdqcVJPvB"
        )
        assert (
            activity.old_token_account == "DbM2nNjaPWJ5NfxYt68QZR2DAtEuXfyA282A5RE6ZXk4"
        )

    def test_parse_transfer_transfer_01(self, load_tx):
        tx = load_tx("transfers", "v1_01")
        mint = "2cQaPyqMaRhU4d9kASVtehNnBYekisjVVf3oTKao3K9E"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "3Z9zoXZPS4NnFkzrMAY6a5KdzfMcRPkrtmNJbtWz2wFU"
        assert (
            activity.new_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )
        assert (
            activity.old_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )

    def test_parse_transfer_transfer_02(self, load_tx):
        tx = load_tx("transfers", "v1_02")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "CXx7CiK43NbhdthMZXA6wC9JPbraLjvZcRwTWuRsLkwH"
        assert (
            activity.new_token_account == "7mTZW2DrvEXcPq5XaT4wRvbqX51CkkNVuA3K8cARy5sx"
        )
        assert (
            activity.old_token_account == "HN5EzbsER7fud5QxhcHXYS8ddVAJgxzoRwMbQJBytbnE"
        )

    def test_parse_transfer_transfer_03(self, load_tx):
        tx = load_tx("transfers", "v1_03")
        mint = "H3g8jr9LD82rWmMoP9NZJVFHqjrpgtcdv3E66EmLwKvX"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "EKkBw5vTqdZfVXYiUb79W1wB1zjyLXKqnuady5SHoG1V"
        assert (
            activity.new_token_account == "EtsBU3Co467oAD1acsMGCGJpx8d78diwss1Sj2d5HhDg"
        )
        assert (
            activity.old_token_account == "53rjSwRTZMvN9yaKfgoBJMsnRgEmmx4quAuQ9GWR8Xuw"
        )

    def test_parse_transfer_unknown_01(self, load_tx):
        tx = load_tx("transfers", "v2_01")
        mint = "FPJtQasfsUmjsJ9pmYVPReNpXMBkVpqavnrcFiWdrx5A"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "9hVanRBfdYvj8WktkBsDeYdmzcpBH85h5vRFp7B2WfoU"
        assert (
            activity.new_token_account == "HFgFM3jHwN9QLUW9tS7iZhEaR51KmshDw9efkAzHPX85"
        )
        assert (
            activity.old_token_account == "JBpgtovoJjVtvHJUA69FeYLhYVhQyZCanzTLAWGBreZq"
        )
