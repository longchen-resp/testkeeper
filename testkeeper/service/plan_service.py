#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:47
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : plan_service.py
@IDE     : PyCharm
------------------------------------
"""
import os
import time
import datetime
from loguru import logger
import threading
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.shell_utils import ShellClient
from testkeeper.service.job_service import JobService
from testkeeper.service.step_service import StepService
from testkeeper.service.plan_status_service import PlanStatusService
from testkeeper.service.job_status_service import JobStatusService
from testkeeper.service.step_status_service import StepStatusService
from testkeeper.exception.exception import *
from typing import Text


class PlanService(SqlInterface):
    def __init__(self):
        super().__init__()
        self.shell_client = ShellClient()
        self.execute_result = {}
        self.job_service = JobService()
        self.step_service = StepService()
        self.plan_status_service = PlanStatusService()
        self.job_status_service = JobStatusService()
        self.step_status_service = StepStatusService()
        self.__limit = 3
        self.__project_name = None
        self.__plan_id = None

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        if limit is None:
            self.__limit = self.__limit
        else:
            if not isinstance(limit, int):
                raise TestKeeperArgvCheckException(f"参数limit:{limit}，类型错误，应当为int or None类型！")
            self.__limit = limit

    @property
    def project_name(self):
        return self.__project_name

    @project_name.setter
    def project_name(self, project_name):
        if project_name is None:
            self.__project_name = self.__project_name
        else:
            if not isinstance(project_name, Text):
                raise TestKeeperArgvCheckException(f"参数project_name:{project_name}，类型错误，应当为str类型！")
            self.__project_name = project_name

    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        if plan_id is None:
            raise TestKeeperArgvCheckException(f"参数planId:{plan_id},类型错误，应当为str类型！")

    def get_test_plan_list(self):
        if self.__project_name is not None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.mul_session.query(TestPlanTable).filter(
                                  TestPlanTable.projectName == self.__project_name).limit(self.__limit).all()]

        else:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.mul_session.query(TestPlanTable).filter().limit(self.__limit).all()]
        return test_plan_list

    def delete_test_plan(self, plan_id: str):
        if plan_id is None:
            logger.warning("plan_id不能为空！")
        else:
            self.get_test_plan_by_id(plan_id).delete()
            self.mul_session.query(TestJobTable).filter_by(planId=plan_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试计划成功:{plan_id}")

    def update_test_plan(self, plan_id: str, name: str, value: str):
        self.common_update_method(TestPlanTable, plan_id, name, value)

    def get_test_plan_by_id(self, plan_id: str) -> TestPlanTable:
        test_plan_table_obj = self.mul_session.query(TestPlanTable).filter(TestPlanTable.id == plan_id).first()
        return test_plan_table_obj

    def get_test_job_list_by_plan_id(self, plan_id: str) -> list:
        test_job_list = self.mul_session.query(TestJobTable).filter_by(planId=plan_id)
        return test_job_list


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                           "db")
    logger.info(db_path)
