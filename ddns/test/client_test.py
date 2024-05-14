from unittest import TestCase

from client import compute_name


class TestClient(TestCase):
    def setUp(self):
        self.domain = "quercusphellos.online"
        self.external = "porkbun.com"
        self.rootname = "quercusphellos.online"
        self.wildcard = "*.quercusphellos.online"
        self.sub = "sub.quercusphellos.online"
        self.supersub = "super.sub.quercusphellos.online"

    def test_compute_name(self):
        with self.assertRaises(ValueError):
            compute_name(self.domain, self.external)

        self.assertEqual("", compute_name(self.domain, self.rootname))
        self.assertEqual("*", compute_name(self.domain, self.wildcard))
        self.assertEqual("", compute_name(self.domain, self.rootname))
        self.assertEqual("sub", compute_name(self.domain, self.sub))
        self.assertEqual("super.sub", compute_name(self.domain, self.supersub))
