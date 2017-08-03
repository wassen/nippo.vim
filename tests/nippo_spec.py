#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest

import os
import sys
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from src.nippo import *

# class TestNippo(unittest.TestCase):
#     def test_arg2daysago(self):
#         self.assertEqual(0, Nippo.arg2daysago("today"))

class TestNippoModule(unittest.TestCase):

    def test_indices(self):
        self.assertEqual([1, 2 ,3], indices(1, [0, 1, 1, 1, 2]))

class TestTask(unittest.TestCase):

    def test___child_tasks_index_list(self):
        self.assertEqual([[1, 2, 4],[],[3],[],[5],[], [7], [8], []],Task._Task__child_tasks_index_list([None, 0, 0, 2, 0, 4, None, 6, 7]))

    def test_parent_task_index_list(self):
        task_depth_list = [0]
        self.assertEqual([None], Task.parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1]
        self.assertEqual([None, 0], Task.parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1, 2]
        self.assertEqual([None, 0, 1], Task.parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1, 1]
        self.assertEqual([None, 0, 0], Task.parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1, 1, 2]
        self.assertEqual([None, 0, 0, 2], Task.parent_task_index_list(task_depth_list))
        task_depth_list = [0, 2, 2, 4, 2, 4, 0, 2, 4]
        self.assertEqual([None, 0, 0, 2, 0, 4, None, 6, 7], Task.parent_task_index_list(task_depth_list))
        task_depth_list = [2, 3, 4, 3, 1, 0, 1]
        self.assertEqual([None, 0, 1, 0, None, None, 5], Task.parent_task_index_list(task_depth_list))

    def test_aaa(self):
        pass
        # func = list
        # itera = ["0", "1", "2"]
        # itera2 = ["0", "1", "2"]
        # task_depth_list = [0, 1, 2]
        # parent_task_index_list = [None, 0, 1]
        # self.assertEqual([None,["0", "0"], ["1", "1"]], Task.aaa(itera,itera2 , task_depth_list, parent_task_index_list, func))

    def test_task_list_from(self):
        lines = ["- [ ] a"]
        res = Task.task_list_from(lines)
        self.assertEqual(1, len(res))
        self.assertEqual(False, Task.task_list_from(lines)[0].completed)

        lines = ["- [ ] a", "- [x] b"]
        res = Task.task_list_from(lines)
        self.assertEqual(2    , len(res))
        self.assertEqual(False, res[0].completed)
        self.assertEqual("a"  , res[0].content)
        self.assertEqual(True , res[1].completed)
        self.assertEqual("b"  , res[1].content)

        lines = ["- [ ] a", "  - [x] b"]
        res = Task.task_list_from(lines)
        self.assertEqual(2     , len(res))
        self.assertEqual(False , res[0].completed)
        self.assertEqual(1, len(res[0].child_tasks))
        self.assertEqual(res[1], res[0].child_tasks[0])
        self.assertEqual(True  , res[1].completed)
        self.assertEqual([] , res[1].child_tasks)

        lines = ["- [ ] a", "- [x] b", "  - [ ] c", "    - [ ] d", "  - [x] e"]
        res = Task.task_list_from(lines)
        self.assertEqual([res[2], res[4]], res[1].child_tasks)
if __name__ == "__main__":
    unittest.main()

