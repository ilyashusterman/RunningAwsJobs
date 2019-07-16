from unittest import TestCase
from pprint import pprint

import botocore

from api.test.aws_api_mock import AwsApiMock
from api.aws_api import AwsApi


class TestAwsApi(TestCase):

    def setUp(self) -> None:
        self.aws_api = AwsApiMock()

    def test_initialize_aws_api(self):
        aws_api = AwsApi()
        pprint(aws_api.__dict__)
