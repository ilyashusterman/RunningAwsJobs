import os

AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_REGION = os.environ.get('AWS_ACCESS_KEY_REGION')
KINESIS_INPUT_STREAM = 'ExampleInputStream'
KINESIS_OUTPUT_STREAM = 'ExampleInputStream'