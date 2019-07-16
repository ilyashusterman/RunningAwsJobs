from api.aws_api import AwsApi


class AwsJobManager:
    """
    Aws async job/tasks managing , handling responses
    """

    def __init__(self):
        self.input_streams = []
        self.api = AwsApi()

    def upload_records(self, records):
        """

        :param records: iterator for s3 Records
        :return:
        """
        input_stream_name = self.create_input_stream()
        responses = []
        for record in records:
            response = self.api.upload_record(
                record=record,
                input_stream_name=input_stream_name
            )

            #TODO generate s3 link

    def create_input_stream(self):
        input_stream_name = self.api.create_new_kinesis_steam(len(self.input_streams))
        self.input_streams.append(input_stream_name)
        return input_stream_name



