from solanalib.parser import SolTransfer, TransferTransaction


class TestTransferTransaction:
    def test_parse_sol_transfer_single(self, load_transfer_tx):
        tx = load_transfer_tx("sales", "mev1_01")
        account = "6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ"
        transfers = tx.parse_sol_transfers(account=account)

        assert len(transfers) == 1
        transfer = transfers[0]
        assert isinstance(transfer, SolTransfer)
        assert transfer.source == "3H3xcs9xwcqaSJm1EV9Mw9ooKqNCVuYTCntzxhdmuLez"
        assert transfer.destination == account
        assert transfer.amount == 1610000000
        assert transfer.program == "MEisE1HzehtrDpAAT8PnLHjpSSkRYakotTuJRPjTpo8"

    def test_parse_sol_transfer_multiple(self, load_transfer_tx):
        tx = load_transfer_tx("sales", "mev1_01")
        account = "3H3xcs9xwcqaSJm1EV9Mw9ooKqNCVuYTCntzxhdmuLez"
        transfers = tx.parse_sol_transfers(account=account)

        assert len(transfers) == 7
        assert all(isinstance(transfer, SolTransfer) for transfer in transfers)

    def test_parse_sol_transfer_all_accounts(self, load_transfer_tx):
        tx = load_transfer_tx("sales", "mev2_01")
        transfers = tx.parse_sol_transfers(account=None)

        assert len(transfers) == 7
        print("\n".join([str(t) for t in transfers]))
        transfer = transfers[0]
        assert all(isinstance(transfer, SolTransfer) for transfer in transfers)
        assert transfers[0].source == "FXA2iPDdHL7cR74vxBb7AgHpqzGFxY9rYXVfqNczZYmF"
        assert transfers[1].source == "659nLL3QmzLmMiUzdgXsnWsCCJagsE8yb51Uu5n4dTfM"
        assert (
            transfers[2].destination == "6ioGtyKjkWUicP6GgbGXLUiTjeXNL2jy5DpCd1jq5pz4"
        )
        assert (
            transfers[3].destination == "A1ApXCwPCSod3ESu6VqtMAUPFpwP94GZR1EuELfoN1Mz"
        )
        assert transfers[4].amount == 60000000
        assert transfers[5].amount == 2640000000
        assert transfers[6].program == "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K"
