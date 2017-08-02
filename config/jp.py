# -*- coding:utf-8 -*-
import vim
import os
day_suffix = "日"
month_suffix = "月"
year_suffix = "年"
nippo_open_error_message = "日報ファイルのオープンに失敗しました。"

vim_nippo_home_directory = "g:nippo#directory"

if vim_nippo_home_directory in vim.vars:
    nippo_directory = os.path.join(vim.eval("g:nippo#home_directory"), "nippo")
else:
    nippo_directory = os.path.join(os.environ["HOME"], "Documents", "nippo")
