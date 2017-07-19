# -*- coding:utf-8 -*-
import os
from datetime import timedelta
from datetime import date

def nippo_today(name="today"):
    print(name)
    # print('日報かけよ {0}'.format(name))
    # vim.command("echo 'Nippo!!!!!!!!!!!!!!!'")
    today = date.today()
    day = str(today.day)
    month = str(today.month)
    year = str(today.year)
    home_dir = os.environ['HOME']
    work_dir = os.path.join(home_dir, "workspace", "plugin")
    nippo_dir = os.path.join(work_dir, year, month, day)
    os.system("mkdir -p {}".format(nippo_dir))
    print(nippo_dir)

def past_date(days):
    return datetime.date.today() - datetime.timedelta(days=days)

# その日の日報を作成して表示
# 昨日のやつを指定して見る
# 今週のやつ
# 会議前に、一週間のやつ
# 昨日のTODOを引き継ぐ

# 型付け不可
# os.mkdirs
