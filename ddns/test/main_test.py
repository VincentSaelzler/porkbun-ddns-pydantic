from unittest import TestCase

from client import PorkbunRecord
from conf import ConfigRecord
from main import list_to_set, model_to_record, models_to_record_set
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
        self.standard_record_set = set(self.standard_records)
        self.standard_porkbun_records = [
            PorkbunRecord(
                id="399347448",
                name="quercusphellos.online",
                type="A",
                content="137.220.108.97",
            ),
            PorkbunRecord(
                id="399348596",
                name="www.quercusphellos.online",
                type="CNAME",
                content="quercusphellos.online",
            ),
        ]
        self.standard_config_records = [
            ConfigRecord(
                name="quercusphellos.online",
                type="A",
                content="137.220.108.97",
            ),
            ConfigRecord(
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

    def test_models_to_record_set(self):
        porkbun_set = models_to_record_set(self.standard_porkbun_records)
        self.assertEqual(porkbun_set, self.standard_record_set)

        config_set = models_to_record_set(self.standard_config_records)
        self.assertEqual(config_set, self.standard_record_set)
