# pylint: skip-file

import io
import test
import unittest

import boto3

BUCKET = "bucket"
FILENAME = "filename.txt"
FILE = (io.BytesIO(b"content"), FILENAME)


class TestFile(test.BaseTestCase):
    def setUp(self):
        self.client = boto3.client(
            "s3",
            access_key_id=self.main.config.get("AWS_ACCESS_KEY_ID"),
            account_id=self.main.config.get("AWS_ACCOUNT_ID"),
            endpoint_url=self.main.config.get("AWS_S3_ENDPOINT"),
            region_name=self.main.config.get("AWS_DEFAULT_REGION"),
            secret_access_key=self.main.config.get("AWS_SECRET_ACCESS_KEY"),
            session_token=self.main.config.get("AWS_SESSION_TOKEN"),
        )

    def tearDown(self):
        response = self.s3_client.list_objects_v2(Bucket=BUCKET)
        if "Contents" in response:
            for content in response["Contents"]:
                self.s3_client.delete_object(Bucket=BUCKET, Key=content["Key"])

    def test_upload_file(self):
        response = self.client.post(f"/file/{bucket}", files={"file": FILE})

        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.data)

    def test_generate_url(self):
        response = self.client.get(f"/file/{BUCKET}/{FILENAME}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("location", response.data)

    def test_delete_file(self):
        response = self.client.delete(f"/file/{BUCKET}/{FILENAME}")

        self.assertEqual(response.status_code, 200)

    def test_upload_duplicate_file(self):
        self.client.post(f"/file/{bucket}", files={"file": FILE})
        response = self.client.post(f"/file/{bucket}", files={"file": FILE})

        self.assertEqual(response.status_code, 201)

    def test_generate_url_deleted_file(self):
        self.client.post(f"/file/{bucket}", files={"file": FILE})
        self.client.delete(f"/file/{BUCKET}/{FILENAME}")
        response = self.client.get(f"/file/{BUCKET}/{FILENAME}")

        self.assertEqual(response.status_code, 404)

    def test_delete_deleted_file(self):
        self.client.post(f"/file/{bucket}", files={"file": FILE})
        self.client.delete(f"/file/{BUCKET}/{FILENAME}")
        response = self.client.delete(f"/file/{BUCKET}/{FILENAME}")

        self.assertEqual(response.status_code, 404)

    def test_generate_url_missing_file(self):
        response = self.client.get(f"/file/{BUCKET}/{FILENAME}")

        self.assertEqual(response.status_code, 404)
