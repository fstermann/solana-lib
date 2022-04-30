from solanalib.nft.activities import MintActivity
from solanalib.nft.transaction import NFTTransaction, Transaction
from solanalib.nft.parse import _handle_input, parse_transaction


class TestParse:
    def test__handle_input_dict(self, load_tx):
        tx = load_tx("mints", "01", as_dict=True)
        mint_token = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        transaction, mint = _handle_input(transaction=tx, mint=mint_token)
        assert isinstance(transaction, Transaction)
        assert not isinstance(transaction, NFTTransaction)
        assert mint == mint_token

    def test__handle_input_Transaction(self, load_tx):
        tx = load_tx("mints", "01")
        mint_token = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        transaction, mint = _handle_input(transaction=tx, mint=mint_token)
        assert isinstance(transaction, Transaction)
        assert not isinstance(transaction, NFTTransaction)
        assert mint == mint_token

    def test__handle_input_NFTTransaction(self, load_tx):
        tx = load_tx("mints", "01", as_dict=True)
        mint_token = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        tx = NFTTransaction(transaction=tx, mint=mint_token)
        transaction, mint = _handle_input(transaction=tx, mint=None)
        assert isinstance(transaction, Transaction)
        assert isinstance(transaction, NFTTransaction)
        assert mint == mint_token

    def test_parse(self, load_tx):
        # The specific parsers are tested in their respective test modules
        tx = load_tx("mints", "01")
        mint_token = "FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC"
        activity = parse_transaction(transaction=tx)
        assert isinstance(activity, MintActivity)
