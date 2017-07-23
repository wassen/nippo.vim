#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
# configへ
nippo_runtime_path = vim.eval("g:nippo#runtime_path")
sys.path.append(nippo_runtime_path)
from src.nippo import Nippo 
def nippo_main(arg="today"):
    Nippo(arg).open()

