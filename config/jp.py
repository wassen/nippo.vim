# -*- coding:utf-8 -*-
import vim
import os
day_suffix = "日"
month_suffix = "月"
year_suffix = "年"
nippo_open_error_message = "日報ファイルのオープンに失敗しました。"

vim_nippo_home_directory = "nippo#directory"

nippo_home_directory = vim.vars.get(
    vim_nippo_home_directory,
    os.path.join(os.environ["HOME"], "Documents")
)

nippo_directory = os.path.join(nippo_home_directory, "nippo")
