# pylint: skip-file

import unittest

# This line also runs `source.service`
# which runs `watchtower.CloudWatchLogHandler`
# that connects to `localstack` and therefore raise connection errors
import source.main


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = source.main.create_main()
        cls.client = cls.main.test_client()
