from api.aws_api import AwsApi
from api.test.RecordGenerator import RecordGenerator

kinesis = AwsApi().kinesis_client

generator = RecordGenerator()
batch_size = 10

records = generator.get_records(batch_size)
# print(records)
response = kinesis.put_records(StreamName="ExampleInputStream", Records=records)
assert response['ResponseMetadata']['HTTPStatusCode'] == 200
print('Records was posted successfully')
