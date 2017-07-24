# -*- coding:utf-8 -*-
import vim
import os
import sys
import traceback
from datetime import timedelta as after
from datetime import date

try:
    nippo_runtime_path = vim.eval("g:nippo#runtime_path")
except NameError:
    nippo_runtime_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(nippo_runtime_path)
from config import jp as config

class Nippo:

    @staticmethod
    def extract_vim_error(error):
        return [line for line in error.split('\n') if line.startswith("vim.error:") ][0].replace("vim.error: Vim(edit):", "")

    @staticmethod
    def call_vim_command(*commands):
        vim.command(":" + " ".join(commands))

    def exists_nippo(self):
        return os.path.isfile(self.nippo_path)

    def open(self):
        os.makedirs(self.nippo_dir, exist_ok=True)

        try:
            Nippo.call_vim_command("silent", "e", self.nippo_path)
        except vim.error:
            sys.stderr.write(Nippo.extract_vim_error(traceback.format_exc()))
            return

        if len(vim.current.buffer) == 1 and vim.current.buffer[0] == "":
            vim.current.buffer[0] = self.nippo_title
            for task in Nippo(self.nippo_date + after(days=-1)).tasks():
                vim.current.buffer.append(task)

    def lines(self):
        with open(self.nippo_path) as nippo_file:
            lines = nippo_file.readlines()
        return lines

    def tasks(self):
        return [line for line in self.lines() if line.startswith("- [ ] ")]

    def __init__(self, nippo_date="today"):
        self.nippo_date  = nippo_date
        self.day         = day        = f"{nippo_date.day}{config.day_suffix}"
        self.month       = month      = f"{nippo_date.month}{config.month_suffix}"
        self.year        = year       = f"{nippo_date.year}{config.year_suffix}"
        self.nippo_dir   = nippo_dir  = os.path.join(config.nippo_home_directory, year, month)
        nippo_name                    = f"{day}.md"
        self.nippo_path               = os.path.join(nippo_dir, nippo_name)
        self.nippo_title              = f"# {year}{month}{day}"

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

# 型付け不可
# os.mkdirs
# xrange 
# import できないんかいfrom src import
