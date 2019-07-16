from api.aws_api import AwsApi


class S3Records:

    def __init__(self, filename, bucket_name):
        self.api = AwsApi()
        self.filename = filename
        self.bucket_name = bucket_name
        self.file_parts = self.api.download_file_parts(self.bucket_name, self.filename)

    def __iter__(self):
        for file_part in self.file_parts:
            yield self.api.download_file_part(file_part)