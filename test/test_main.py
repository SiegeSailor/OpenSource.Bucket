# pylint: skip-file

import test
import unittest


class TestMain(test.BaseTestCase):
    def test_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_fallback(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)
