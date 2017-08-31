#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest

import os
import sys
from datetime import date
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

# *つかいたい
from src.nippo import indices
from src.nippo import Nippo
from src.nippo import Task
from src.nippo import Tasks

# class TestNippo(unittest.TestCase):
#     def test_arg2daysago(self):
#         self.assertEqual(0, Nippo.arg2daysago("today"))


class TestNippoModule(unittest.TestCase):

    def test_indices(self):
        self.assertEqual([1, 2, 3], indices(1, [0, 1, 1, 1, 2]))


class TestNippo(unittest.TestCase):

    def test_Nippo(self):
        year  = 2000
        month = 2
        day   = 2
        nippo = Nippo(date(year, month, day))
        self.assertEqual("# 2000年2月2日", nippo.title)


class TestTask(unittest.TestCase):

    def test_child_tasks_index_list(self):
        self.assertEqual([[1, 2, 4], [], [3], [], [5], [], [7], [8], []], Task._Task__child_tasks_index_list([None, 0, 0, 2, 0, 4, None, 6, 7]))

    def test_parent_task_index_list(self):
        task_depth_list = [0]
        self.assertEqual([None], Task._Task__parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1]
        self.assertEqual([None, 0], Task._Task__parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1, 2]
        self.assertEqual([None, 0, 1], Task._Task__parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1, 1]
        self.assertEqual([None, 0, 0], Task._Task__parent_task_index_list(task_depth_list))
        task_depth_list = [0, 1, 1, 2]
        self.assertEqual([None, 0, 0, 2], Task._Task__parent_task_index_list(task_depth_list))
        task_depth_list = [0, 2, 2, 4, 2, 4, 0, 2, 4]
        self.assertEqual([None, 0, 0, 2, 0, 4, None, 6, 7], Task._Task__parent_task_index_list(task_depth_list))
        task_depth_list = [2, 3, 4, 3, 1, 0, 1]
        self.assertEqual([None, 0, 1, 0, None, None, 5], Task._Task__parent_task_index_list(task_depth_list))

    def test_aaa(self):
        pass
        # func = list
        # itera = ["0", "1", "2"]
        # itera2 = ["0", "1", "2"]
        # task_depth_list = [0, 1, 2]
        # _Task__parent_task_index_list = [None, 0, 1]
        # self.assertEqual([None,["0", "0"], ["1", "1"]], Task.aaa(itera,itera2 , task_depth_list, _Task__parent_task_index_list, func))

    def test_task_list_from(self):
        lines = ["- [ ] a"]
        res = Task.task_list_from(lines)
        self.assertEqual(1    , len(res))
        self.assertEqual(False, res[0].completed)
        self.assertEqual(None , res[0].date)

        lines = [
            "# 2017年8月21日",
            "- [ ] a",
            "# 2017年9月22日",
            "- [x] b"
        ]
        res = Task.task_list_from(lines)
        self.assertEqual(2    , len(res))
        self.assertEqual(False, res[0].completed)
        self.assertEqual("a"  , res[0].content)
        self.assertEqual(21   , res[0].date.day)
        self.assertEqual(True , res[1].completed)
        self.assertEqual("b"  , res[1].content)
        self.assertEqual(22   , res[1].date.day)

        lines = ["- [ ] a", "  - [x] b"]
        res = Task.task_list_from(lines)
        self.assertEqual(1    , len(res))
        self.assertEqual(False, res[0].completed)
        self.assertEqual(1    , len(res[0].child_tasks))
        self.assertEqual(True , res[0].child_tasks[0].completed)
        self.assertEqual([]   , res[0].child_tasks[0].child_tasks)

        lines = ["- [ ] a", "- [x] b", "  - [ ] c", "    - [ ] d", "  - [x] e"]
        res = Task.task_list_from(lines)
        self.assertEqual("c", res[1].child_tasks[0].content)
        self.assertEqual("e", res[1].child_tasks[1].content)


class TestTasks(unittest.TestCase):
    def test_expand_task(self):
        # dependent on Task
        lines = ["- [ ] a", "- [x] b", "  - [ ] c", "    - [ ] d", "  - [x] e"]
        task_list = Task.task_list_from(lines)
        # 楽にインスタンス生成したい
        res = Tasks()
        res.extend(task_list)
        tasks = res._Tasks__expand_task_tree()
        self.assertEqual("a", tasks[0].content)
        self.assertEqual("b", tasks[1].content)
        self.assertEqual("c", tasks[2].content)
        self.assertEqual("d", tasks[3].content)
        self.assertEqual("e", tasks[4].content)

if __name__ == "__main__":
    unittest.main()

