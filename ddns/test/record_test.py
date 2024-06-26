from copy import deepcopy
from unittest import TestCase

from client import PorkbunRecord
from main import model_to_record
from model import Record

# the Record type is hashable because
# it is frozen and all of its fields are hashable
# pyright: reportUnhashable=false


class TestSetOperations(TestCase):
    """
    Confirm that the model.Record class functions as expected
    with regard to set operations
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


class TestDictOperations(TestCase):
    """
    Confirm that the model.Record class functions as expected
    with regard to set operations
    """

    def setUp(self):
        self.porkbun_a = PorkbunRecord(
            id="399347448",
            name="quercusphellos.online",
            type="A",
            content="137.220.108.97",
        )
        self.a = model_to_record(self.porkbun_a)
        self.a_copy = deepcopy(self.a)
        self.porkbun_cname = PorkbunRecord(
            id="399348596",
            name="www.quercusphellos.online",
            type="CNAME",
            content="quercusphellos.online",
        )
        self.cname = model_to_record(self.porkbun_cname)
        self.existing_records = {
            self.a: self.porkbun_a,
            self.cname: self.porkbun_cname,
        }
        self.existing_records_duplicated = {
            self.a: self.porkbun_a,
            self.a_copy: self.porkbun_a,
            self.cname: self.porkbun_cname,
        }
        self.ftwenty = Record(
            name="quercusphellos.online", type="A", content="4.20.4.20"
        )
        self.fun_records = {self.ftwenty, self.cname}
        self.desired_records = {
            self.a,
            self.cname,
        }

    def test_hashable_keys(self):
        self.assertEqual(self.existing_records, self.existing_records_duplicated)

    def test_create(self):
        create = self.fun_records - self.existing_records.keys()
        ftwentyset = {self.ftwenty}
        self.assertEqual(create, ftwentyset)

    def test_no_action(self):
        matching_keys = self.desired_records & self.existing_records.keys()
        matching = [self.existing_records[key] for key in matching_keys]
        self.assertEqual(len(matching), len(self.existing_records))

    def test_delete(self):
        delete = self.existing_records.keys() - self.fun_records
        aset = {self.a}
        self.assertEqual(delete, aset)
