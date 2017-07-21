# -*- coding:utf-8 -*-
import os
import sys
import traceback
from datetime import timedelta
from datetime import date

nippo_runtime_path = vim.eval("g:nippo#runtime_path")
sys.path.append(nippo_runtime_path)
from config import jp as config

nippo_home_directory = vim.eval("g:nippo#directory")

def open_nippo(period="today"):

    def make_nippo_file(nippo_path):
        with open(nippo_path, 'w') as nippo_file:
            nippo_file.write(nippo_title())

    def nippo_title():
        return "# {}{}{}".format(year, month, day)

    day_suffix = "日"
    month_suffix = "月"
    year_suffix = "年"

    if "today".startswith(period):
        d = date.today()
    elif "yesterday".startswith(period):
        d = past_date(1)
    else:
        try:
            d = past_date(int(period))
        except ValueError:
            print("invarid argument")

    day = str(d.day) + day_suffix
    month = str(d.month) + month_suffix
    year = str(d.year) + year_suffix
    nippo_name = day + ".md"
    nippo_dir = os.path.join(nippo_home_directory, year, month)
    nippo_path = os.path.join(nippo_dir, nippo_name)

    os.makedirs(nippo_dir, exist_ok=True)
    # make_nippo_file(nippo_path)
    try:
        call_vim_command("silent", "e", nippo_path)
    except vim.error:
        sys.stderr.write(extract_vim_error(traceback.format_exc()))
        return

    if not os.path.isfile(nippo_path):
            vim.current.buffer[0] = nippo_title()


def extract_vim_error(error):
    return [line for line in error.split('\n') if line.startswith("vim.error:")][0]

def past_date(days):
    return date.today() - timedelta(days=days)

def call_vim_command(*commands):
    vim.command(":" + " ".join(commands))

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
