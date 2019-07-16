import boto


class AwsApi:

    def __init__(self):
        """
        Connects to aws with exported environment variables
        """
        self.ec2_client = boto.connect_ec2()
        self.s3_client = boto.connect_s3()

