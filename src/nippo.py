# -*- coding:utf-8 -*-
import os
from datetime import timedelta
from datetime import date

nippo_home_directory = vim.eval("g:nippo#directory")

def open_nippo(period="today"):

    def make_nippo_file(nippo_path):
        if os.path.isfile(nippo_path):
            return
        with open(nippo_path, 'w') as nippo_file:
            nippo_file.write(nippo_title())

    def nippo_title():
        return "# {}{}{}".format(year, month, day)

    day_suffix = "日"
    month_suffix = "月"
    year_suffix = "年"
    d = date.today()
    day = str(d.day) + day_suffix
    month = str(d.month) + month_suffix
    year = str(d.year) + year_suffix
    nippo_name = day + ".md"
    nippo_dir = os.path.join(nippo_home_directory, year, month)
    nippo_path = os.path.join(nippo_dir, nippo_name)

    os.makedirs(nippo_dir, exist_ok=True)
    make_nippo_file(nippo_path)
    nippo_call_vim_command("silent", "e", nippo_path)


def nippo_past_date(days):
    return datetime.date.today() - datetime.timedelta(days=days)

def nippo_call_vim_command(*commands):
    vim.command(":" + " ".join(commands))

# その日の日報を作成して表示
# 昨日のやつを指定して見る
# 今週のやつ
# 会議前に、一週間のやつ
# 昨日のTODOを引き継ぐ

# 型付け不可
# os.mkdirs
# xrange 
