# -*- coding:utf-8 -*-
import os
import sys
import vim
day_suffix = "日"
month_suffix = "月"
year_suffix = "年"
nippo_open_error_message = "日報ファイルのオープンに失敗しました。"
try:
    try:
        nippo_home_directory = os.path.join(vim.eval("g:nippo#directory"), "nippo")
    except vim.error:
        nippo_home_directory = os.path.join(os.environ["HOME"], "Documents", "nippo")
except NameError:
    nippo_home_directory = os.path.join(os.environ["HOME"], "Documents", "nippo")
