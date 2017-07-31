#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest

import os
import sys
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from src.nippo import Nippo
from src.nippo import Task

# class TestNippo(unittest.TestCase):
#     def test_arg2daysago(self):
#         self.assertEqual(0, Nippo.arg2daysago("today"))

class TestTask(unittest.TestCase):
    def test_task_list_from(self):
        lines = ""
        self.assertEqual([], Task.task_list_from(lines))
        lines = "- [ ] task1"
        self.assertEqual(False, Task.task_list_from(lines)[].completed)

if __name__ == "__main__":
    unittest.main()

