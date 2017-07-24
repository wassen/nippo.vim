#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from datetime import timedelta
from datetime import date

try:
    nippo_runtime_path = vim.eval("g:nippo#runtime_path")
except NameError:
    nippo_runtime_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(nippo_runtime_path)
from src.nippo import Nippo


def nippo_main(arg="today"):

    def parse_arg(arg):
        # tasks done this week
        if "today".startswith(arg):
            return date.today()
        elif "yesterday".startswith(arg):
            return date.today() + timedelta(days=-1)
        else:
            try:
                return date.today() - timedelta(days=int(arg))
            except ValueError:
                print("invarid argument")

    Nippo(parse_arg(arg)).open()

