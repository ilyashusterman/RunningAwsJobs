from unittest import TestCase
from pprint import pprint

import botocore

from api.test.record_generator import RecordGenerator
from api.test.aws_api_mock import AwsApiMock
from api.aws_api import AwsApi


class TestAwsApi(TestCase):

    def setUp(self) -> None:
        self.aws_api = AwsApiMock()

    def test_initialize_aws_api(self):
        aws_api = AwsApi()
        pprint(aws_api.__dict__)

    def test_create_kinesis_stream(self):
        aws_api = AwsApi()
        input_stream_name = aws_api.create_new_kinesis_steam(stream_num=0)
        generator = RecordGenerator()
        batch_size = 10

        records = generator.get_records(batch_size)
        with aws_api.upload_records(records=records, input_stream_name=input_stream_name) as response:
            self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
