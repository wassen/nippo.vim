#!/usr/bin/env python
# -*- coding:utf-8 -*-
import vim
import os
from os.path import join
import sys
from datetime import timedelta
from datetime import date

nippo_runtime_path = vim.eval("g:nippo#runtime_path")
sys.path.append(nippo_runtime_path)
from src.config import jp as config
from src.nippo import Nippo, Tasks, Task


def nippo_main(arg="today"):

    # Nippo tasks done this weekとか
    def tasks():
        Tasks(join(config.nippo_directory, "tasks")).open()

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
            print("invalid argument")


def nippo_tasks():

    # Nippo tasks done this weekとか
    def tasks():
        Tasks.load().open()

    tasks()


def nippo_add_task():
    def is_path_inside_directory(path, directory):
        return os.path.realpath(path).startswith(os.path.realpath(directory))

    file_path = vim.current.buffer.name
    if not is_path_inside_directory(file_path, config.nippo_directory):
        return

    tasks_file = join(config.nippo_directory, "tasks")
    tasks = Tasks.load(tasks_file)

    task_list = Task.task_list_from(vim.current.buffer)

    tasks.extend(task_list)
    tasks.save()


def nippo_update_tasks():

    # file access every changing text in vim
    tasks = Tasks()
    task_list = Task.task_list_from(vim.current.buffer)
    tasks.extend(task_list)
    tasks.save()

def nippo_show_tasks():
    pass
