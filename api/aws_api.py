import os
import subprocess
import logging
from contextlib import contextmanager

import boto3
import botocore

from api.config import KINESIS_INPUT_STREAM
from api.s3_file_part import FilePart


class AwsApi:
    """ shared object that could me asynchronously run in threads as declared via lock object """
    s3_client = boto3.client('s3')

    def __init__(self):
        """
        Connects to aws with exported environment variables
        """
        self.kinesis_client = boto3.client('kinesis')

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

    def get_file_links(self, bucket_name):
        return self.s3_client.list_objects(Bucket=bucket_name)['Contents']

    def download_file_parts(self, bucket_name, filename):
        return self.s3_client.download_file_parts(bucket_name, filename)

    def get_file_parts(self, filename, bucket_name, min_part_size=1):
        """

        :param filename:
        :param bucket_name:
        :return: Generator for file parts
        """
        return (self.get_file_part(link, bucket_name) for link in self.get_file_links(bucket_name)
                if self.is_link_valid(link, filename, min_part_size))

    def is_link_valid(self, link, filename, min_part_size):
        if link['Size'] < min_part_size:
            return False
        else:
            return filename in link['Key']

    def get_file_part(self, link, bucket_name):
        filepart = FilePart.from_link(link)
        self.download_link(bucket_name, filepart.s3_url, filepart.local_filename)
        return filepart

    def download_link(cls, bucket_name, key_path, filename):
        return cls.s3_client.download_file(bucket_name,
                                            key_path, os.path.join(os.curdir, filename))