from solanalib.rpc.client import Client
from solanalib.util import make_list_batches


class ProClient(Client):
    def get_all_parsed_transactions_for_address(self, account: str):
        signatures = self.get_all_signatures_for_address(account=account)

        BATCH_SIZE = 50
        batches = make_list_batches(signatures, BATCH_SIZE)
        all_transactions = []

        for batch in batches:
            responses = self.get_transactions(transaction_signatures=batch)
            all_transactions += responses

        return all_transactions

    def get_all_signatures_for_address(self, account: str):
        before = None
        fetched_all = False
        limit = 1000
        all_signatures = []

        while not fetched_all:
            response = self.get_signatures_for_address(
                account=account, limit=limit, before=before
            )
            signatures = [info["signature"] for info in response["result"]]
            all_signatures += signatures

            if len(signatures) < limit:
                fetched_all = True

            before = signatures[-1]

        return all_signatures
