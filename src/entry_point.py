#!/usr/bin/env python
# -*- coding:utf-8 -*-
import vim
import os
from os.path import join
import sys
import pickle
from datetime import timedelta
from datetime import date

nippo_runtime_path = vim.eval("g:nippo#runtime_path")
sys.path.append(nippo_runtime_path)
from config import jp as config
from src.nippo import Nippo, Tasks, Task

def nippo_main(arg="today"):

    # Nippo tasks done this weekとか
    def tasks():
        Tasks(join(config.nippo_home_directory, "tasks")).open()

    def nippo(date):
        Nippo(date).open()

    if "tasks".startswith(arg):
        tasks()
    elif "today".startswith(arg):
        nippo(date.today())
    elif "yesterday".startswith(arg):
        nippo(date.today() - timedelta(days=1))
    else:
        try:
            nippo(date.today() - timedelta(days=int(arg)))
        except ValueError:
            print("invarid argument")

def nippo_tasks():

    # Nippo tasks done this weekとか
    def tasks():
        Tasks.load().open()

    tasks()

def nippo_add_task():

    tasks_file = join(config.nippo_home_directory, "tasks")
    tasks = Tasks.load(tasks_file)

    task_list = Task.task_list_from(vim.current.buffer)

    tasks.extend(task_list)
    tasks.save()

    # with open(join(config.nippo_home_directory, "tasks"), "bw") as f:
    #     pickle.dump(tasks, f)

def nippo_update_tasks():

    # file access every changing text in vim
#    tasks_file = join(config.nippo_home_directory, "tasks")
#    tasks = Tasks.load(tasks_file)

    # if not tasks.tasks. == tasks:

    tasks = Tasks()
    task_list = Task.task_list_from(vim.current.buffer)
    tasks.extend(task_list)
    tasks.save()

def nippo_show_tasks():
    pass
