import boto3

# Modify this section to reflect your AWS configuration.

class AwsApi:

    def __init__(self):
        """
        Connects to aws with exported environment variables
        """
        # self.s3_client = boto.connect_s3()
        self.kinesis_client = boto3.client('kinesis')

