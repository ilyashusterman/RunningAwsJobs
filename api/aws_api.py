import logging
import subprocess
from contextlib import contextmanager

import boto3
import botocore

from api.config import KINESIS_INPUT_STREAM


class AwsApi:

    def __init__(self):
        """
        Connects to aws with exported environment variables
        """
        self.kinesis_client = boto3.client('kinesis')
        self.s3_client = boto3.client('s3')

    @contextmanager
    def upload_records(self, records, input_stream_name=KINESIS_INPUT_STREAM):
        try:
            yield self.kinesis_client.put_records(StreamName=input_stream_name, Records=records)
        except Exception as e:
            #TODO check via test for failing upload to stream
            #should be code to release resource
            pass
        finally:
            """Release resource"""

    @contextmanager
    def upload_record(self, record, input_stream_name=KINESIS_INPUT_STREAM):
        try:
            yield self.kinesis_client.put_record(
                stream_name=input_stream_name,
                data=record['data'],
                partition_key=record['partition_key']
            )
        except Exception as e:
            #TODO check via test for failing upload to stream
            #should be code to release resource
            pass
        finally:
            """Release resource"""

    def create_new_kinesis_steam(self, stream_num):
        """
        running cli command
        aws kinesis create-stream \
        --stream-name ExampleInputStream \
        --shard-count 1 \
        --region us-west-2 \
        :return:
        """
        input_stream_name = 'input_stream_%s' % stream_num
        try:
            subprocess.run(["aws", "kinesis", "create-stream",
                            "--stream-name", input_stream_name,
                            "--shard-count", "1"])
        except Exception as e:
            #TODO shoold rase create stream exception
            raise Exception('Create Stream Exception')
        else:
            return input_stream_name

    def upload_file(self, file_path, file_name, bucket, folder):
        """
        Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param folder: path of folder within bucket
        :return: upload file response
        """
        try:
            yield self.s3_client.upload_file(file_path, bucket, '{}/{}'.format(folder, file_name))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "403":
                logging.error("Forbidden access , bucket: {}".format(bucket))
            else:
                logging.error("Error occourd while uploading file, file name: {},  bucket: {}".format(file_name, bucket))
        else:
            logging.info("Succesfuly uploaded file: {} into bucket: {}".format(file_name, bucket))

    def get_files(self, bucket_name):
        return self.s3_client.list_objects(Bucket=bucket_name)['Contents']

    def download_file_parts(self, bucket_name, filename):
        return self.s3_client.download_file_parts(bucket_name, filename)

    def download_file_part(self, file_part):
        #TODO
        pass

    def get_file(self, filename, bucket_name, part_size=64000):
        """

        :param filename:
        :param bucket_name:
        :return: Generator for file parts
        """