# pylint: skip-file

import io
import logging
import test
import unittest

import boto3


class TestFile(test.BaseTestCase):
    def setUp(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.main.config.get("AWS_ACCESS_KEY_ID"),
            aws_account_id=self.main.config.get("AWS_ACCOUNT_ID"),
            endpoint_url=self.main.config.get("AWS_S3_ENDPOINT"),
            region_name=self.main.config.get("AWS_DEFAULT_REGION"),
            aws_secret_access_key=self.main.config.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=self.main.config.get("AWS_SESSION_TOKEN"),
        )

    def tearDown(self):
        buckets = self.s3.list_buckets()["Buckets"]
        for bucket in buckets:
            items = self.s3.list_objects_v2(Bucket=bucket["Name"])
            if "Contents" in items:
                for item in items["Contents"]:
                    self.s3.delete_object(Bucket=bucket["Name"], Key=item["Key"])
            self.s3.delete_bucket(Bucket=bucket["Name"])

    def test_upload_file(self):
        response = self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.data.decode())

    def test_generate_url(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )
        response = self.client.get(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 200)
        self.assertIn("location", response.data.decode())

    def test_delete_file(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )
        response = self.client.delete(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 200)

    def test_generate_nonexistent_file_url(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.png")},
            content_type="multipart/form-data",
        )
        response = self.client.get(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 404)

    def test_generate_nonexistent_bucket_url(self):
        response = self.client.get(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_file(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.png")},
            content_type="multipart/form-data",
        )
        response = self.client.delete(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_bucket(self):
        response = self.client.delete(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 404)

    def test_upload_duplicate_file(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )
        response = self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 201)

    def test_generate_url_deleted_file(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )
        self.client.delete(f"/file/dummy-bucket/filename.txt")
        response = self.client.get(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 404)

    def test_delete_deleted_file(self):
        self.client.post(
            f"/file/dummy-bucket",
            data={"file": (io.BytesIO(b"content"), "filename.txt")},
            content_type="multipart/form-data",
        )
        self.client.delete(f"/file/dummy-bucket/filename.txt")
        response = self.client.delete(f"/file/dummy-bucket/filename.txt")

        self.assertEqual(response.status_code, 404)
