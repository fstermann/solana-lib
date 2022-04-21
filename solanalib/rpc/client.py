import json
from typing import List, Union

import requests

from .endpoints import Endpoint
from .methods import MethodBuilder
from .parameter import Commitment, Encoding
from solanalib.logger import logger


class Client:
    endpoint: Union[Endpoint, str] = Endpoint.DEFAULT
    method_builder: MethodBuilder = None

    def __init__(self, endpoint: Union[Endpoint, str] = Endpoint.DEFAULT):
        self.endpoint = endpoint
        self.method_builder = MethodBuilder()

    def _make_request(self, payload):
        logger.debug(f"Making request to {self.endpoint.url}")
        logger.debug(f"Payload: {payload}")

        response = requests.post(self.endpoint.url, json=payload)
        json_response = response.json()
        return json_response

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
