# -*- coding:utf-8 -*-
import vim
import os
import sys
import pickle
import traceback
from datetime import timedelta as after
from datetime import date

try:
    nippo_runtime_path = vim.eval("g:nippo#runtime_path")
except NameError:
    nippo_runtime_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(nippo_runtime_path)
from config import jp as config

def call_vim_command(*commands):
    vim.command(":" + " ".join(commands))

def extract_vim_error(error):
    return [line for line in error.split('\n') if line.startswith("vim.error:") ][0].replace("vim.error: Vim(edit):", "")

class TaskOfFile:
    def tasks(self):
        return [line for line in self.lines() if line.startswith("- [ ] ")]

    def lines(self):
        with open(self.nippo_path) as nippo_file:
            return nippo_file.readlines()

class NippoFile(TaskOfFile):
    def __init__(self, nippo_path):
        # nippo以外にディレクトリにフォルダなりがあるとバグるよ
        self.nippo_path = nippo_path

class Nippo(TaskOfFile):

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

        if len(vim.current.buffer) == 1 and vim.current.buffer[0] == "":
            vim.current.buffer[0] = self.nippo_title
            # for task in Nippo(self.nippo_date + after(days=-1)).tasks():
            #     vim.current.buffer.append(task)

    def __init__(self, nippo_date="today"):
        self.nippo_date  = nippo_date
        self.day         = day        = f"{nippo_date.day}{config.day_suffix}"
        self.month       = month      = f"{nippo_date.month}{config.month_suffix}"
        self.year        = year       = f"{nippo_date.year}{config.year_suffix}"
        self.nippo_dir   = nippo_dir  = os.path.join(config.nippo_home_directory, year, month)
        nippo_name                    = f"{day}.md"
        self.nippo_title              = f"# {year}{month}{day}"
        self.nippo_path               = os.path.join(nippo_dir, nippo_name)

class Task:

    # taskオブジェクトがやることか？
    # 0行目ないときはえらーだぞ
    def title(self):
        return self.lines[0]

    # 最初の一個だけかよ
    def tasks(self):
        return [line for line in self.lines if line.startswith("- [ ] ")][0]

    def __init__(self, date, title, content):
        self.date    = date
        self.title   = title
        self.content = content

class Tasks:
    def append(self, task):
        tasks_same_day = [self_task for self_task in self.tasks if self_task.date == task.date]
        print(tasks_same_day)
        print(task.content)
        if all([not task_same_day.content == task.content for task_same_day in tasks_same_day]):
            self.tasks.append(task)

    def extend(self, task_list):
        for task in task_list:
            self.append(task)

    def open(self):
        try:
            call_vim_command("silent", "e", os.devnull)
            vim.current.buffer.append([task.content for task in self.tasks])
            del vim.current.buffer[0]

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

        tasks_path = os.path.join(config.nippo_home_directory, "tasks")
        if os.path.isfile(tasks_path):
            with open(tasks_path, "br") as f:
                return pickle.load(f)
        else:
            return Tasks(tasks_path=tasks_path)

    def __init__(self, **kwargs):
        self.tasks = kwargs.get("tasks", [])
        self.tasks_path = kwargs.get("tasks_path", os.path.join(config.nippo_home_directory, "tasks"))







# class Tasks:
#     def __init__(self, tasks_path):
#         self.tasks_path = tasks_path
#         nippo_files = [NippoFile(os.path.join(root, file_))
#                 for root, _, files in os.walk(config.nippo_home_directory)
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

# 型付け不可
# os.mkdirs
# xrange 
# import できないんかいfrom src import

# wをフックしてオブジェクトに書き込む
# オブジェクトから自動的に読み込んで、タスクに反映(削除は扱いが難しいから今のところ無しで)
