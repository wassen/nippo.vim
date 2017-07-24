#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest

import os
import sys
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from src.nippo import Nippo as Nippo

class TestNippo(unittest.TestCase):
    def test_arg2daysago(self):
        self.assertEqual(0, Nippo.arg2daysago("today"))

if __name__ == "__main__":
    unittest.main()

