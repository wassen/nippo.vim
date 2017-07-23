# -*- coding:utf-8 -*-
import os
import sys
import traceback
from datetime import timedelta
from datetime import date

nippo_runtime_path = vim.eval("g:nippo#runtime_path")
sys.path.append(nippo_runtime_path)
from config import jp as config

class Nippo:

    @staticmethod
    def arg2daysago(arg):
        if "today".startswith(arg):
            return 0
        elif "yesterday".startswith(arg):
            return 1
        else:
            try:
                return int(arg)
            except ValueError:
                print("invarid argument")

    @staticmethod
    def date_from(daysago):
        return date.today() - timedelta(days=daysago)

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

        if not self.exists_nippo():
            vim.current.buffer[0] = self.nippo_title

    def __init__(self, arg="today"):
        self.nippo_date = nippo_date = Nippo.date_from(daysago=Nippo.arg2daysago(arg))
        self.day        = day        = f"{nippo_date.day}{config.day_suffix}"
        self.month      = month      = f"{nippo_date.month}{config.month_suffix}"
        self.year       = year       = f"{nippo_date.year}{config.year_suffix}"
        self.nippo_dir  = nippo_dir  = os.path.join(config.nippo_home_directory, year, month)
        nippo_name                   = f"{day}.md"
        self.nippo_path              = os.path.join(nippo_dir, nippo_name)
        self.nippo_title             = f"# {year}{month}{day}"

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

# 型付け不可
# os.mkdirs
# xrange 
