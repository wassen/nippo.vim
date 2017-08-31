# -*- coding:utf-8 -*-
import vim
import os
import sys
import re
import pickle
import traceback
import datetime
from datetime import date
from collections import defaultdict

try:
    nippo_runtime_path = vim.eval("g:nippo#runtime_path")
except NameError:
    nippo_runtime_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(nippo_runtime_path)
from src.config import jp as config


def call_vim_command(*commands):
    vim.command(":" + " ".join(commands))


def indices(value, it):
    return [i for i, e in enumerate(it) if e == value]


def extract_vim_error(error):
    return [line for line in error.split('\n') if line.startswith("vim.error:")][0].replace("vim.error: Vim(edit):", "")

class Vim():
    @staticmethod
    def is_new_buffer():
        return len(vim.current.buffer) == 1 and vim.current.buffer[0] == ""

    def replace_all_lines(lines):
        del vim.current.buffer[:]
        vim.current.buffer.append(lines)
        del vim.current.buffer[0]


class Nippo:
    # ここでバグらない不思議
    @staticmethod
    def exists_nippo(self):
        return os.path.isfile(self.nippo_path)

    def open(self):
        os.makedirs(self.nippo_dir, exist_ok=True)

        try:
            call_vim_command("silent", "e", self.nippo_path)
        except vim.error:
            sys.stderr.write(extract_vim_error(traceback.format_exc()))
            return

        if Vim.is_new_buffer():
            lines = [self.title]
            lines.append("")
            lines.extend(self.templete_for_office)
            Vim.replace_all_lines(lines)

    def __init__(self, nippo_date=date.today()):
        self.nippo_date  = nippo_date
        self.day         = day        = f"{nippo_date.day}{config.day_suffix}"
        self.month       = month      = f"{nippo_date.month}{config.month_suffix}"
        self.year        = year       = f"{nippo_date.year}{config.year_suffix}"
        self.nippo_dir   = nippo_dir  = os.path.join(config.nippo_directory, year, month)
        nippo_name                    = f"{day}.md"
        self.title                    = f"# {year}{month}{day}"
        self.templete_for_office      = [
            "<!--外向け日報-->",
            self.nippo_date.strftime(f"# %Y/%m/%d_{config.name}"),
            "## <Templete subject>",
            "SETUP: ",
            "CONFRONT: ",
            "RESOLVE: ",
        ]
        self.nippo_path               = os.path.join(nippo_dir, nippo_name)


class Task:
    PREFIX_NOT_COMPLETED = "- [ ] "
    PREFIX_COMPLETED     = "- [x] "

    @staticmethod
    def __child_tasks_index_list(parent_task_index_list):
        return [indices(i, parent_task_index_list) for i, x in enumerate(parent_task_index_list)]

    @staticmethod
    def __parent_task_index_list(task_depth_list):
        parent_task_index_list = []
        for i, task_depth in enumerate(task_depth_list):
            is_shallower_task_list = [task_depth > other_task_depth for other_task_depth in task_depth_list[:i]]
            parent_task_index = [j for j, is_deeper_task in enumerate(is_shallower_task_list) if is_deeper_task][-1:]
            if not len(parent_task_index) == 0:
                parent_task_index_list.append(parent_task_index[0])
            else:
                parent_task_index_list.append(None)
        return parent_task_index_list

    @staticmethod
    def __task_tree(task_dicts, child_tasks_index_list):

        def task_tree(current_depth):
            if current_depth < 0:
                return [x for (x, d) in zip(res, task_depth_list) if min_depth == d]
            else:
                for i in indices(current_depth, task_depth_list):
                    j = child_tasks_index_list[i]
                    res[i] = Task(task_dicts[i]["date"], task_dicts[i]["depth"], task_dicts[i]["completed"], task_dicts[i]["content"], child_tasks=[res[k] for k in j])
                return task_tree(current_depth - 1)

        # Noneのリストではなくオブジェクトとして扱う、とか？
        res = [None] * len(task_dicts)
        task_depth_list = [task_dict["depth"] for task_dict in task_dicts]
        if not len(res) == 0:
            min_depth = min(task_depth_list)
            max_depth = max(task_depth_list)
            return task_tree(max_depth)
        else:
            return []

    @classmethod
    def task_list_from(cls, lines):
        def task_reg(line):
            # starting, 0 or more blanks, "- [", blank or x "] "
            return re.search("^\s*-\s\[[x\s]\]\s", line)

        def date_reg(line):
            return re.search(f"^#\s\d+{config.year_suffix}\d+{config.month_suffix}\d+{config.day_suffix}", line)

        def parse_date(line):
            try:
                return datetime.datetime.strptime(line, '# %Y年%m月%d日').date()
            except ValueError:
                print("invalid line")

        def task_depth(line):
            r = task_reg(line)
            if r is None:
                return None
            const = 6
            depth = r.end() - const
            return depth

        def task_content(line):
            r = task_reg(line)
            if r is None:
                return None
            # strip - [ ]
            content = line.lstrip(r.group())
            return content

        def task_completed(line):
            r = task_reg(line)
            if r is None:
                return False
            return "x" in r.group()

        def task_date(task_index, index_date):
            def smaller_max(number, number_list):
                for i in reversed(sorted(number_list)):
                    if i < number:
                        return i
            index = smaller_max(task_index, index_date.keys())
            if index is not None:
                return index_date[index]

        index_date = {i: parse_date(line) for i, line in enumerate(lines) if date_reg(line)}
        task_dicts = [{"date": task_date(i, index_date), "content": task_content(line), "depth": task_depth(line), "completed": task_completed(line)}
                for i, line in enumerate(lines) if task_reg(line) is not None]

        task_depth_list = [task_dict["depth"] for task_dict in task_dicts]

        parent_task_index_list = cls.__parent_task_index_list(task_depth_list)
        child_tasks_index_list = cls.__child_tasks_index_list(parent_task_index_list)

        res = cls.__task_tree(task_dicts, child_tasks_index_list)

        return res

    def to_displayable(self):
        return " " * self.depth + self.prefix + self.content

    def __eq__(self, other):
        if other is None or not type(self) == type(other):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        return iter(self.child_tasks)

    def __len__(self):
        return len(self.child_tasks)

    def __init__(self, date, depth, completed, content, **kwargs):
        self.child_tasks      = kwargs.get("child_tasks", None)
        self.date             = date
        self.depth            = depth
        self.completed        = completed
        self.content          = content
        self.prefix = self.__class__.PREFIX_COMPLETED if completed else self.__class__.PREFIX_NOT_COMPLETED


class Tasks():
    # tasksは list を継承するべきだった
    # parent_nodeってだけなので、実コンテンツを持たないタスクみたいな扱いにしたい
    tasks_file = os.path.join(config.nippo_directory, ".tasks.nptsk")

    def append(self, task):
        if all([not self_task == task for self_task in self.tasks]):
            self.tasks.append(task)

    def extend(self, task_list):
        for task in task_list:
            self.append(task)

    @staticmethod
    def __expand_task(l, task):
        l.append(task)
        if not len(task) == 0:
            for child in task:
                Tasks.__expand_task(l, child)

    def __expand_task_tree(self):
        l = []
        for task in self:
            Tasks.__expand_task(l, task)
        return l

    def to_displayable(self):
        tasks = self.__expand_task_tree()
        date_task = defaultdict(list)
        for task in tasks:
            date_task[task.date].append(task)

        result = []
        for date_ in date_task:
            if date_:
                result.append((f"# {date_.year}{config.year_suffix}{date_.month}{config.month_suffix}{date_.day}{config.day_suffix}"))
            else:
                result.append(f"Unknown date")
            result.extend([task.to_displayable() for task in date_task[date_]])
        return result


    def open(self):
        try:
            call_vim_command("silent", "e", self.__class__.tasks_file)
            Vim.replace_all_lines(self.to_displayable())
        except vim.error:
            sys.stderr.write(extract_vim_error(traceback.format_exc()))
            return

    def save(self, tasks_path=None):

        if tasks_path is None:
            tasks_path = self.tasks_path

        with open(self.tasks_path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(tasks_path=None):

        tasks_path = os.path.join(config.nippo_directory, "tasks")
        if os.path.isfile(tasks_path):
            with open(tasks_path, "br") as f:
                return pickle.load(f)
        else:
            return Tasks(tasks_path=tasks_path)

    def __iter__(self):
        return iter(self.tasks)

    def __init__(self, **kwargs):
        self.tasks = kwargs.get("tasks", [])
        self.tasks_path = kwargs.get("tasks_path", os.path.join(config.nippo_directory, "tasks"))

# class Tasks:
#     def __init__(self, tasks_path):
#         self.tasks_path = tasks_path
#         nippo_files = [NippoFile(os.path.join(root, file_))
#                 for root, _, files in os.walk(config.nippo_directory)
#                     for file_ in files if ".md"
#                         in file_ and not file_.startswith(".")]
#
#         nippo_tasks = []
#         for nippo_file in nippo_files:
#             tasks = nippo_file.tasks()
#             if not len(tasks) == 0:
#                 nippo_tasks.append("title\n")
#             for task in nippo_file.tasks():
#                 nippo_tasks.append(task)
#
#         with open(tasks_path, 'w') as f:
#             f.writelines(nippo_tasks)
#

    # def pre_write(self):
    #     call_vim_command
    #         self.previous_buffer =


# その日の日報を作成して表示
# 昨日のやつを指定して見る
# 今週のやつ
# 会議前に、一週間のやつ
# 昨日のTODOを引き継ぐ
# 既に開かれていたらバグる
# class Buffer
# print(config.nippo_open_error_message)
# 1.5ヶ月前とか
# 特定の日付とか
# day_as_word
# Nippo tasks 全タスク表示
# Nippo init 全ファイル網羅してファイル
# vimでpdb？デバッグ使いにくい
# テンプレート

# 型付け不可
# os.mkdirs
# xrange
# import できないんかいfrom src import

# wをフックしてオブジェクトに書き込む
# オブジェクトから自動的に読み込んで、タスクに反映(削除は扱いが難しいから今のところ無しで)




