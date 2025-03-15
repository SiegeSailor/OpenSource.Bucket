# pylint: skip-file

import unittest

import source.main


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = source.main.create_main()
        cls.client = cls.main.test_client()
