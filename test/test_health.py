# pylint: skip-file


import test


class TestHealth(test.BaseTestCase):
    def test_health(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
