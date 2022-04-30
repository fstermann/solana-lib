from typing import List, Union

import requests
from ratelimit import limits, sleep_and_retry
from solanalib.logger import logger

from .endpoints import Endpoint
from .methods import MethodBuilder
from .parameter import Commitment, Encoding, TransactionDetails


class Client:
    endpoint: Union[Endpoint, str] = Endpoint.DEFAULT
    method_builder: MethodBuilder = None

    def __init__(
        self, endpoint: Union[Endpoint, str] = Endpoint.DEFAULT, ratelimit: int = 20
    ):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.method_builder = MethodBuilder()
        self.ratelimit = limits(calls=ratelimit, period=1)

    def _make_request(self, payload):
        @sleep_and_retry
        @self.ratelimit
        def _make_request_limited():
            logger.debug(f"Making request to {self.endpoint.url}")
            payload_string = f"{str(payload)[:10]}...{str(payload)[-10:]}"
            payload_len = len(payload) if isinstance(payload, list) else 1
            logger.debug(
                f"Payload ({payload_len} call{'' if payload_len == 1 else 's'}): {payload_string}"
            )

            response = self.session.post(self.endpoint.url, json=payload)

            logger.debug(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.debug(response.text)

            json_response = response.json()
            return json_response

        return _make_request_limited()

    def health_check(self):
        pass

    def get_transaction(
        self,
        transaction_signature: str,
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = self.method_builder.get_transaction(
            transaction_signature=transaction_signature,
            encoding=encoding,
            commitment=commitment,
        )
        return self._make_request(payload)

    def get_transactions(
        self,
        transaction_signatures: List[str],
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = [
            self.method_builder.get_transaction(
                transaction_signature=transaction_signature,
                encoding=encoding,
                commitment=commitment,
            )
            for transaction_signature in transaction_signatures
        ]
        return self._make_request(payload)

    def get_token_largest_accounts(
        self,
        token_mint: str,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = self.method_builder.get_token_largest_accounts(
            token_mint=token_mint,
            commitment=commitment,
        )
        return self._make_request(payload)

    def get_signatures_for_address(
        self,
        account: str,
        limit: int = 1000,  # between 1 and 1000
        before: str = None,
        until: str = None,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = self.method_builder.get_signatures_for_address(
            account=account,
            limit=limit,
            before=before,
            until=until,
            commitment=commitment,
        )
        return self._make_request(payload)

    def get_account_info(
        self,
        account: str,
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = self.method_builder.get_account_info(
            account=account,
            encoding=encoding,
            commitment=commitment,
        )
        return self._make_request(payload)

    def get_block(
        self,
        slot: int,
        encoding: Encoding = Encoding.JSON_PARSED,
        transaction_details: TransactionDetails = TransactionDetails.FULL,
        rewards: bool = True,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = self.method_builder.get_block(
            slot=slot,
            encoding=encoding,
            transaction_details=transaction_details,
            rewards=rewards,
            commitment=commitment,
        )
        return self._make_request(payload)
