from api.aws_api import AwsApi
from api.test.record_generator import RecordGenerator

api = AwsApi()

generator = RecordGenerator()
batch_size = 10

records = generator.get_records(batch_size)
with api.upload_records(records=records) as response:
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    print(f'{len(records)} Records were posted successfully')
