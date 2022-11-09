#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 22:43
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : test_cmd.py
@IDE     : PyCharm
------------------------------------
"""
import sys
import os
import unittest
from ddt import ddt, data
from testkeeper.client import entry


@ddt
class TestCmd(unittest.TestCase):
    def test_show_version(self):
        sys.argv = ["Tk", "-V"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_load_help(self):
        sys.argv = ["Tk", "plan_load", "-h"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_help(self):
        sys.argv = ["Tk", "plan_show", "-h"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_all(self):
        sys.argv = ["Tk", "plan_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_by_limit(self):
        sys.argv = ["Tk", "plan_show", "-l", "10"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show(self):
        sys.argv = ["Tk", "plan_show", "-p", "测试项目1", "-l", "10"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_project_is_none(self):
        sys.argv = ["Tk", "plan_show", "-l"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_show(self):
        sys.argv = ["Tk", "job_show", "-p_id", "3"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_plan_id_is_none(self):
        sys.argv = ["Tk", "job_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_delete_plan(self):
        sys.argv = ["Tk", "plan_delete", "-plan_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_plan(self):
        sys.argv = ["Tk", "plan_update", "-plan_id", "7", "-name", "executeScriptCmd", "-value",
                    "sleep 30 && echo test"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_start(self):
        sys.argv = ["Tk", "plan_start", "-plan_id", "8"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
