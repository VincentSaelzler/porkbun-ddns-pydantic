from unittest import TestCase

from main import list_to_set
from model import Record


class TestMain(TestCase):
    def setUp(self):
        self.duplicate_records = [
            Record(name="quercusphellos.online", type="A", content="137.220.108.97"),
            Record(name="quercusphellos.online", type="A", content="137.220.108.97"),
        ]
        self.standard_records = [
            Record(name="quercusphellos.online", type="A", content="137.220.108.97"),
            Record(
                name="www.quercusphellos.online",
                type="CNAME",
                content="quercusphellos.online",
            ),
        ]

    def test_list_to_set_fail(self):
        with self.assertRaises(ValueError):
            _ = list_to_set(self.duplicate_records)

    def test_list_to_set_pass(self):
        standard_set = set(self.standard_records)
        deduplicated_set = list_to_set(self.standard_records)
        self.assertEqual(standard_set, deduplicated_set)
