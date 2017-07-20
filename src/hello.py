# -*- coding:utf-8 -*-
import os
from datetime import timedelta
from datetime import date

nippo_home_directory =  vim.eval("g:nippo#directory")

def nippo_today(name="today"):
    day_suffix = "日"
    month_suffix = "月"
    year_suffix = "年"
    today = date.today()
    day = str(today.day) + day_suffix
    month = str(today.month) + month_suffix
    year = str(today.year) + year_suffix
    nippo_file = day + ".md"
    nippo_dir = os.path.join(nippo_home_directory, year, month)
    nippo_path = os.path.join(nippo_dir, nippo_file)

    os.makedirs(nippo_dir, exist_ok=True)
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

