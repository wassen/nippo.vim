#!/usr/bin/env python
# -*- coding:utf-8 -*-
# this is mock module
import os


def eval(string):
    if string == "g:nippo#runtime_path":
        return os.path.abspath(os.path.dirname(__file__))
    elif string == "g:nippo#home_directory":
        return os.path.join(os.environ["HOME"], "Documents")
    else:
        return "mock string"


class error(Exception):
    pass


if __name__ == "__main__":
    print('This "vim" module is pseudo.')
