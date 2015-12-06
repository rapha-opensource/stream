from unittest import TestCase
from os import environ

from boto3 import resource

from stream import BotoStreamingIO

class TestBasic(TestCase):

    def setUp(self):
        if 'AWS_ACCESS_KEY_ID' not in environ or 'AWS_SECRET_ACCESS_KEY' not in environ:
            raise EnvironmentError('AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in the environment')
        self.s3 = resource('s3')
        self.bucket = self.s3.create_bucket(Bucket='__stream__'+self.id())

    def tearDown(self):
        for key in self.bucket.objects.all():
            key.delete()
        self.bucket.delete()

    def test_basic(self):
        expected_content = 'yomama'.encode('utf-8')
        s3_object = self.bucket.put_object(Key='test_key', Body=expected_content)
        s3_object.wait_until_exists()

        read_obj = self.bucket.Object('test_key')
        response = read_obj.get()
        io = BotoStreamingIO(response['Body'], read_obj.content_length)
        
        content = io.read()

        self.assertEqual(content, expected_content)

