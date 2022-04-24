from solanalib.nft.parsers.transfers import parse_transfer
from solanalib.nft.models import TransferActivity
from unittest import mock


class TestParseTransfers:
    def test_parse_transfer_outer_inner_01(self, load_tx):
        # Transfers twice in 1 tx, once in the outer ix, once in the inner
        tx = load_tx("transfers", "outer_inner_01")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert (
            activity.old_token_account == "DbM2nNjaPWJ5NfxYt68QZR2DAtEuXfyA282A5RE6ZXk4"
        )
        assert (
            activity.new_token_account == "EyEc7WEWJ6BNhY1QEeJnHAqC8fZuywm8PW3LRntEBr8b"
        )
        assert activity.old_authority == "7JvFNAjVNXN9aABtgggELpQr7UreL5i3AtjhzTWcNcTo"
        assert activity.new_authority == "9VarrpaH6KyAnhCFLxW69Am8gtXGEC9oHy8rJCTwZtqp"

    def test_parse_transfer_transferChecked_01(self, load_tx):
        # Is transferred by transferChecked
        # the new_authority is not mentioned in the tx
        tx = load_tx("transfers", "transferChecked_01")
        mint = "2cQaPyqMaRhU4d9kASVtehNnBYekisjVVf3oTKao3K9E"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert (
            activity.old_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )
        assert (
            activity.new_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )
        assert (
            activity.old_token_account == "B9U6Ftt4Vqg9f6xvXg1PD3sfc84t776eG6Upxo8dxDPJ"
        )
        assert activity.old_authority == "3Z9zoXZPS4NnFkzrMAY6a5KdzfMcRPkrtmNJbtWz2wFU"
        # assert activity.new_authority == "3Z9zoXZPS4NnFkzrMAY6a5KdzfMcRPkrtmNJbtWz2wFU"
        # TODO Need to check for the treu new authority, this one is False

    def test_parse_transfer_transferChecked_02(self, load_tx):
        # Is transferred by transferChecked
        # the new_authority is mentioned in the tx post/pre token balances
        tx = load_tx("transfers", "transferChecked_02")
        mint = "Ge2L2Bt8CPsVEFRZBKSu5dCnz746i7ukbBCpAsPv44VL"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint

        assert (
            activity.old_token_account == "HN5EzbsER7fud5QxhcHXYS8ddVAJgxzoRwMbQJBytbnE"
        )
        assert (
            activity.new_token_account == "7mTZW2DrvEXcPq5XaT4wRvbqX51CkkNVuA3K8cARy5sx"
        )
        assert activity.old_authority == "CXx7CiK43NbhdthMZXA6wC9JPbraLjvZcRwTWuRsLkwH"
        assert activity.new_authority == "3n7c3AoQP75hdeJBS43D3rucuj4MSPQt1RWommbxrR8G"

    def test_parse_transfer_outer_setAuthority(self, load_tx):
        # Transfers once in outer ix, new authority is set
        tx = load_tx("transfers", "outer_setAuthority")
        mint = "H3g8jr9LD82rWmMoP9NZJVFHqjrpgtcdv3E66EmLwKvX"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert (
            activity.old_token_account == "53rjSwRTZMvN9yaKfgoBJMsnRgEmmx4quAuQ9GWR8Xuw"
        )
        assert (
            activity.new_token_account == "EtsBU3Co467oAD1acsMGCGJpx8d78diwss1Sj2d5HhDg"
        )
        assert activity.old_authority == "EKkBw5vTqdZfVXYiUb79W1wB1zjyLXKqnuady5SHoG1V"
        assert activity.new_authority == "JwYEQBgkKFi9nQymFm8ouG8n4fBqYFASE52kK9KfeBM"

    def test_parse_transfer_inner_01(self, load_tx):
        # Transfers once in inner ix
        tx = load_tx("transfers", "inner_01")
        mint = "FPJtQasfsUmjsJ9pmYVPReNpXMBkVpqavnrcFiWdrx5A"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert (
            activity.old_token_account == "JBpgtovoJjVtvHJUA69FeYLhYVhQyZCanzTLAWGBreZq"
        )
        assert (
            activity.new_token_account == "HFgFM3jHwN9QLUW9tS7iZhEaR51KmshDw9efkAzHPX85"
        )
        assert activity.old_authority == "9hVanRBfdYvj8WktkBsDeYdmzcpBH85h5vRFp7B2WfoU"
        assert activity.new_authority == "2KBxCTCvwQnumQPcXY1Ty414upiQkoPM75hykaRqnzED"

    def test_parse_transfer_inner_multisigAuthority(self, load_tx):
        # Transfers once in inner, old owner is in mutlisig authority
        tx = load_tx("transfers", "inner_multisigAuthority")
        mint = "FPJtQasfsUmjsJ9pmYVPReNpXMBkVpqavnrcFiWdrx5A"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint
        assert (
            activity.old_token_account == "9JMbXbN6WkTsYxn9dErLmgWkj8yMxQZZvmT4vHihLLtw"
        )
        assert (
            activity.new_token_account == "GXN4jrxPHhNzq4aWKixALSTtiZeg5AJUZXxbjUBQUZro"
        )
        assert activity.old_authority == "F4ghBzHFNgJxV4wEQDchU5i7n4XWWMBSaq7CuswGiVsr"
        assert activity.new_authority == "6Y7HG1cWWhgS1jiagpi5YQQLsmvuGsUTyt6ETcuERX3t"

    @mock.patch("solanalib.nft.parsers.transfers.Client.get_account_info")
    def test_parse_transfer_inner_without_init_or_create(
        self, mock_Client_get_account_info, load_tx, load_account_info
    ):
        account_info = load_account_info(
            "transfers", "Ccuxg9SibF4eohijB5s9EvBxoSCEpVzLiQLG6B3Rih6m"
        )
        mock_Client_get_account_info.return_value = account_info
        # Transfers once in inner
        # Token account already exists, no init or create statement
        tx = load_tx("transfers", "inner_without_init_or_create")
        mint = "4mSvhZ4CCWixrYkwHjL6yVCoURn2U8xoXN7zbpakzMck"
        activity = parse_transfer(tx=tx, mint=mint)
        assert isinstance(activity, TransferActivity)
        assert activity.mint == mint

        assert (
            activity.old_token_account == "EcV6E3e35LSi3CByjnJEsjd3MpLYz5ZnhXeAxFCVpgt6"
        )
        assert (
            activity.new_token_account == "Ccuxg9SibF4eohijB5s9EvBxoSCEpVzLiQLG6B3Rih6m"
        )
        assert activity.old_authority == "4pUQS4Jo2dsfWzt3VgHXy3H6RYnEDd11oWPiaM2rdAPw"
        assert activity.new_authority == ""
