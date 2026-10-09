"""Regression tests for mt.gpu.get_mem_info."""

import unittest
from unittest import mock

import mt.gpu


class TestGetMemInfo(unittest.TestCase):
    def test_source_is_repo(self):
        self.assertTrue(mt.gpu.__file__.startswith("/home/minhtri/gitcentre/mtgpu/"))

    def test_tk1_returns_none(self):
        with mock.patch.object(mt.gpu, "detect_machine", return_value="arm64-tk1"):
            self.assertIsNone(mt.gpu.get_mem_info())
            self.assertIsNone(mt.gpu.get_mem_info(print_bars=True))

    def test_unknown_returns_none(self):
        with mock.patch.object(mt.gpu, "detect_machine", return_value="unknown"):
            self.assertIsNone(mt.gpu.get_mem_info())


if __name__ == "__main__":
    unittest.main()
