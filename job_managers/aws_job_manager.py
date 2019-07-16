import logging

from api.aws_api import AwsApi
from api.s3_records import S3Records

MAX_RECORD_FAILURES = 3

class AwsJobManager:
    """
    Aws async job/tasks managing , handling responses
    1. Create kineses stream
    2. Once the stream is ready- checks if process didnt failed
    3.put some data into the stream - put records.
    4.read records from an S3 file.
    5. Apply some kind of processing on the data read (whatever you like) and
        write the result file to S3.
    6. Client checks if exists by 400 response generated s3 link url
    """

    def __init__(self):
        self.input_streams = []
        self.api = AwsApi()

    def get_s3_records(self, filename, bucket_name):
        """

        :param filename:
        :param bucket_name:
        :return: generator for records dataframe
        """
        return S3Records(filename=filename, bucket_name=bucket_name)

    def process_records(self, records):
        """
        do some processing
        :param records:
        :return:
        """
        return (self.process_single_record(record) for record in records)

    def process_single_record(self, record_df):
        record_df['test_col'] = 'test_process'
        return record_df

    def upload_processed_records(self, records):
        """

        :param records: generator for s3 Records
        :return:
        """
        input_stream_name = self.create_input_stream()
        failed_records = []
        for index, record in enumerate(records):
            try:
                self.api.upload_record(
                    record=record,
                    input_stream_name=input_stream_name
                )
            except Exception as e:
                logging.error('Failed to upload %s record' % index)
                failed_records.append(index)

        self.upload_stream_to_s3(input_stream_name)
        if len(failed_records) > 0:
            logging.error('%s Errors occured to upload records' % len(failed_records))
        else:
            logging.info('Uploaded successfully no errors')



            #TODO generate s3 link

    def create_input_stream(self):
        """
        process does not take long , but could fail via api timeout
        TODO test on few more streams with other regions and shard-count parameters
        :return:
        """
        num_stream = len(self.input_streams)
        input_stream_name = self.api.create_new_kinesis_steam(num_stream)
        self.input_streams.append(input_stream_name)
        return input_stream_name

    def upload_stream_to_s3(self, input_stream_name):
        """
        from uploaded kinesis aws client transfer the data to s3
        :param input_stream_name:
        :return:
        """
        #TODO implement on aws cloud



