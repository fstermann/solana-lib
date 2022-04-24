from solanalib.nft.parsers.transfers import parse_transfer
from solanalib.nft.models import TransferActivity


class TestParseTransfers:
    def test_parse_transfer_transferChecked_01(self, load_tx):
        tx = load_tx("transfers", "v0_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "9VarrpaH6KyAnhCFLxW69Am8gtXGEC9oHy8rJCTwZtqp"
        assert (
            activity.new_token_account == "EyEc7WEWJ6BNhY1QEeJnHAqC8fZuywm8PW3LRntEBr8b"
        )
        assert (
            activity.old_token_account == "DbM2nNjaPWJ5NfxYt68QZR2DAtEuXfyA282A5RE6ZXk4"
        )
        assert activity.old_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"

    def test_parse_transfer_transfer_01(self, load_tx):
        tx = load_tx("transfers", "v1_01")
        mint = "2cQaPyqMaRhU4d9kASVtehNnBYekisjVVf3oTKao3K9E"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.old_authority == "3Z9zoXZPS4NnFkzrMAY6a5KdzfMcRPkrtmNJbtWz2wFU"
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
        assert activity.old_authority == "CXx7CiK43NbhdthMZXA6wC9JPbraLjvZcRwTWuRsLkwH"
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
        assert activity.old_authority == "EKkBw5vTqdZfVXYiUb79W1wB1zjyLXKqnuady5SHoG1V"
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
        assert activity.new_authority == "2KBxCTCvwQnumQPcXY1Ty414upiQkoPM75hykaRqnzED"
        assert (
            activity.new_token_account == "HFgFM3jHwN9QLUW9tS7iZhEaR51KmshDw9efkAzHPX85"
        )
        assert (
            activity.old_token_account == "JBpgtovoJjVtvHJUA69FeYLhYVhQyZCanzTLAWGBreZq"
        )

    def test_parse_transfer_unknown_02(self, load_tx):
        tx = load_tx("transfers", "v3_01")
        mint = "FPJtQasfsUmjsJ9pmYVPReNpXMBkVpqavnrcFiWdrx5A"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert activity.new_authority == "6Y7HG1cWWhgS1jiagpi5YQQLsmvuGsUTyt6ETcuERX3t"
        assert (
            activity.new_token_account == "GXN4jrxPHhNzq4aWKixALSTtiZeg5AJUZXxbjUBQUZro"
        )
        assert (
            activity.old_token_account == "9JMbXbN6WkTsYxn9dErLmgWkj8yMxQZZvmT4vHihLLtw"
        )

    # def test_parse_transfer_unknown_03(self, load_tx):
    #     tx = load_tx("transfers", "v4_01")
    #     mint = "4mSvhZ4CCWixrYkwHjL6yVCoURn2U8xoXN7zbpakzMck"
    #     activity = parse_transfer(tx=tx, mint=mint)
    #     assert isinstance(activity, TransferActivity)
    #     assert activity.mint == mint
    #     # assert activity.new_authority == "6Y7HG1cWWhgS1jiagpi5YQQLsmvuGsUTyt6ETcuERX3t"
    #     assert (
    #         activity.new_token_account == "Ccuxg9SibF4eohijB5s9EvBxoSCEpVzLiQLG6B3Rih6m"
    #     )
    #     assert (
    #         activity.old_token_account == "EcV6E3e35LSi3CByjnJEsjd3MpLYz5ZnhXeAxFCVpgt6"
    #     )
