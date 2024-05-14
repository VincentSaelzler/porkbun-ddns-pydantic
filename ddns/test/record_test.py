from copy import deepcopy
from unittest import TestCase

from model import Record


class TestSetOperations(TestCase):
    """
    Confirm that the model.Record class functions as expected
    with regard to set and dict operations
    """

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
        self.standard_records_copy = deepcopy(self.standard_records)
        self.standard_records_backwards = [
            Record(
                name="www.quercusphellos.online",
                type="CNAME",
                content="quercusphellos.online",
            ),
            Record(name="quercusphellos.online", type="A", content="137.220.108.97"),
        ]
        self.fun_records = [
            Record(name="quercusphellos.online", type="A", content="4.20.4.20"),
            Record(
                name="www.quercusphellos.online",
                type="CNAME",
                content="quercusphellos.online",
            ),
        ]

    def test_remove_dupe(self):
        distinct_records = set(self.duplicate_records)
        self.assertEqual(len(distinct_records), 1)

    def test_keep_distinct(self):
        distinct_records = set(self.standard_records)
        self.assertEqual(len(distinct_records), 2)

    def test_copy_equal(self):
        standard_set = set(self.standard_records)
        copy_set = set(self.standard_records_copy)
        self.assertEqual(standard_set, copy_set)

    def test_backwards_equal(self):
        standard_set = set(self.standard_records)
        backward_set = set(self.standard_records_backwards)
        self.assertEqual(standard_set, backward_set)

    def test_intersection(self):
        standard_set = set(self.standard_records)
        fun_set = set(self.fun_records)
        intersection = standard_set & fun_set
        expected_intersection = set(
            [
                Record(
                    name="www.quercusphellos.online",
                    type="CNAME",
                    content="quercusphellos.online",
                ),
            ]
        )
        self.assertEqual(intersection, expected_intersection)

    def test_symmetric_difference(self):
        standard_set = set(self.standard_records)
        fun_set = set(self.fun_records)
        symmetric_difference = standard_set ^ fun_set
        expected_symmetric_difference = set(
            [
                Record(name="quercusphellos.online", type="A", content="4.20.4.20"),
                Record(
                    name="quercusphellos.online", type="A", content="137.220.108.97"
                ),
            ]
        )
        self.assertEqual(symmetric_difference, expected_symmetric_difference)

    def test_no_difference(self):
        standard_set = set(self.standard_records)
        copy_set = set(self.standard_records_copy)
        symmetric_difference = standard_set ^ copy_set
        self.assertEqual(len(symmetric_difference), 0)
        self.assertEqual(symmetric_difference, set())
