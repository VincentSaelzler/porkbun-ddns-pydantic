import unittest

from main import EditableRecord


class TestEditableRecords(unittest.TestCase):
    def setUp(self):

        self.duplicate_records = [
            EditableRecord(
                name="quercusphellos.online", type="A", content="137.220.108.97"
            ),
            EditableRecord(
                name="quercusphellos.online", type="A", content="137.220.108.97"
            ),
        ]
        self.standard_records = [
            EditableRecord(
                name="quercusphellos.online", type="A", content="137.220.108.97"
            ),
            EditableRecord(
                name="www.quercusphellos.online", type="CNAME", content="quercusphellos.online"
            ),
        ]

    def test_remove_dupe(self):
        distinct_records = set(self.duplicate_records)
        self.assertEqual(len(distinct_records), 1)

    def test_keep_distinct(self):
        distinct_records = set(self.standard_records)
        self.assertEqual(len(distinct_records), 2)