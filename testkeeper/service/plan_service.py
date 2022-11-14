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
import json
import time
import datetime
from loguru import logger
import asyncio
import threading
from testkeeper.service.sql_interface import SqlInterface
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable
from testkeeper.module.execute_status_module import ExecuteStatus
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from testkeeper.util.shell_utils import ShellClient
from testkeeper.util.system_info import SystemInfo


class PlanService(SqlInterface):
    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}

    def get_test_plan_list(self, project_name: str = None, limit: int = 3):
        if project_name is not None and limit is not None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.sqlSession.query(TestPlanTable).filter(
                                  TestPlanTable.projectName == project_name).limit(limit).all()]
        elif project_name is None and limit is not None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.sqlSession.query(TestPlanTable).filter().limit(limit).all()]
        elif project_name is not None and limit is None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.sqlSession.query(TestPlanTable).filter(
                                  TestPlanTable.projectName == project_name).limit(limit).all()]
        else:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.sqlSession.query(TestPlanTable).filter().limit(limit).all()]
        return test_plan_list

    def get_test_plan_status_list(self, project_name: str = None, limit: int = 3):
        if project_name is not None and limit is not None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.sqlSession.query(TestPlanStatusTable).filter(
                                         TestPlanTable.projectName == project_name).limit(limit).all()]
        elif project_name is None and limit is not None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.sqlSession.query(TestPlanStatusTable).filter().limit(limit).all()]
        elif project_name is not None and limit is None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.sqlSession.query(TestPlanStatusTable).filter(
                                         TestPlanTable.projectName == project_name).limit(limit).all()]
        else:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.sqlSession.query(TestPlanStatusTable).filter().limit(limit).all()]
        return test_plan_status_list

    def delete_test_plan(self, plan_id: str):
        if plan_id is None:
            logger.warning("plan_id不能为空！")
        else:
            logger.info(plan_id)
            logger.info(self.sqlSession.query(TestPlanTable).filter(TestPlanTable.id == plan_id).first())
            self.sqlSession.query(TestPlanTable).filter_by(id=plan_id).delete()
            self.sqlSession.query(TestJobTable).filter_by(planId=plan_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试计划成功:{plan_id}")

    def delete_test_job(self, job_id: str):
        if job_id is None:
            logger.warning("job_id不能为空！")
        else:
            logger.info(job_id)
            self.sqlSession.query(TestJobTable).filter_by(id=job_id).delete()
            self.sqlSession.query(TestStepTable).filter_by(jobId=job_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试任务成功:{job_id}")

    def delete_test_step(self, step_id: str):
        if step_id is None:
            logger.warning("step_id不能为空！")
        else:
            logger.info(step_id)
            self.sqlSession.query(TestStepTable).filter_by(id=step_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试步骤成功:{step_id}")

    def delete_test_plan_status(self, plan_status_id: str):
        if plan_status_id is None:
            logger.warning("plan_id不能为空！")
        else:
            logger.info(plan_status_id)
            self.sqlSession.query(TestPlanStatusTable).filter_by(id=plan_status_id).delete()
            self.sqlSession.query(TestJobStatusTable).filter_by(planStatusID=plan_status_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试计划成功:{plan_status_id}")

    def delete_test_job_status(self, job_status_id: str):
        if job_status_id is None:
            logger.warning("job_id不能为空！")
        else:
            logger.info(job_status_id)
            self.sqlSession.query(TestJobStatusTable).filter_by(id=job_status_id).delete()
            self.sqlSession.query(TestStepStatusTable).filter_by(jobId=job_status_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试任务成功:{job_status_id}")

    def delete_test_step_status(self, step_status_id: str):
        if step_status_id is None:
            logger.warning("step_status_id不能为空！")
        else:
            logger.info(step_status_id)
            self.sqlSession.query(TestStepStatusTable).filter_by(id=step_status_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试步骤成功:{step_status_id}")

    def update_test_plan(self, plan_id: str, name: str, value: str):
        self.common_update_method(TestPlanTable, plan_id, name, value)

    def update_test_job(self, job_id: str, name: str, value: str):
        self.common_update_method(TestJobTable, job_id, name, value)

    def common_update_method(self, table_obj, update_id: str, name: str, value: str):
        table_obj_instance = self.sqlSession.query(table_obj).filter_by(id=update_id).first()
        logger.info(table_obj_instance.__repr__())
        if name in table_obj_instance.__dict__:
            table_obj_instance.__setattr__(name, value)
            table_obj_instance.updateTime = datetime.datetime.now()
            self.sqlSession.commit()
        else:
            raise Exception(f"修改的key:{name} 不存在")

    def update_test_plan_status(self, plan_status_id, name: str, value: str):
        self.common_update_method(TestPlanStatusTable, plan_status_id, name, value)

    def update_test_job_status(self, job_status_id: str, name: str, value: str):
        self.common_update_method(TestJobStatusTable, job_status_id, name, value)

    def update_test_step(self, step_id: str, name: str, value: str):
        self.common_update_method(TestStepTable, step_id, name, value)

    def update_test_step_status(self, step_status_id: str, name: str, value: str):
        self.common_update_method(TestStepStatusTable, step_status_id, name, value)

    def add_test_plan(self, file_path: str):
        ...

    def execute_test_plan(self, plan_id: str):
        test_plan = self.sqlSession.query(TestPlanTable).filter_by(id=plan_id).first()
        test_job_list = self.sqlSession.query(TestJobTable).filter_by(id=plan_id).all()
        test_plan_status_table_obj = TestPlanStatusTable(
            id=test_plan.id,
            planName=test_plan.planName,
            planId=test_plan.id,
            executeStatus=ExecuteStatus.RUNNING,
            updateTime=datetime.datetime.now(),
            createTime=datetime.datetime.now()
        )
        for test_job in test_job_list:
            self.execute_test_job(test_plan_status_table_obj, test_job, test_job.id)
        self.sqlSession.add(test_plan_status_table_obj)
        self.sqlSession.commit()

    def execute_cmd(self, test_job):
        logger.info("#####")
        self.execute_result = self.shell_client.run_cmd(
            f"cd {test_job.executeScriptPath} && {test_job.executeScriptCmd}",
            timeout=600)

    def watch_execute_cmd_process(self, test_job, test_job_status_table_obj):
        time.sleep(test_job.checkInterval)
        pid = SystemInfo.get_process_pid_by_os(self.shell_client, test_job.executeScriptCmd)
        while True:
            try:
                process_is_exists, process_is_status = SystemInfo.get_process_status(test_job.executeScriptCmd, pid)
                if process_is_exists is not True and process_is_status != "running":
                    test_job_status_table_obj.executeStatus = ExecuteStatus.EXCEPTION
                    break
                else:
                    logger.info(f"任务{test_job.jobName}正在运行中，检查周期{test_job.checkInterval}s,运行状态:{process_is_status}")
            except Exception as e:
                logger.info(f"任务{test_job.jobName}执行结束，结束监听")
                break
            time.sleep(test_job.checkInterval)

    def check_execute_cmd(self, test_job, test_job_status_table_obj):
        execute_cmd_thread = threading.Thread(target=self.execute_cmd, args=(test_job,))
        execute_cmd_thread.setDaemon(True)
        watch_execute_cmd_process_thread = threading.Thread(target=self.watch_execute_cmd_process,
                                                            args=(test_job, test_job_status_table_obj))
        watch_execute_cmd_process_thread.setDaemon(True)
        execute_cmd_thread.start()
        watch_execute_cmd_process_thread.start()
        watch_execute_cmd_process_thread.join()

    def execute_test_job(self, test_plan_status_table_obj, test_job: TestJobTable, job_id: str):
        test_job = self.get_test_job(job_id) if test_job is None else test_job
        test_job_status_table_obj = TestJobStatusTable(
            jobId=test_job.id,
            jobName=test_job.jobName,
            executeStatus=ExecuteStatus.RUNNING,
            executeMachineIp="127.0.0.1",
            logFilePath="/tmp",
            processPid=11,
            updateTime=datetime.datetime.now(),
            createTime=datetime.datetime.now()
        )
        if test_job.isSkipped:
            logger.info(f"跳过当前执行的任务{test_job.jobName}")
            test_job_status_table_obj.executeStatus = ExecuteStatus.SKIPPED
        else:
            logger.info(f"正在执行任务：{test_job.jobName}")
            self.check_execute_cmd(test_job, test_job_status_table_obj)
            if test_job.runFailedIsNeedContinue is not True and self.execute_result["ret"] != 0:
                test_job_status_table_obj.executeStatus = ExecuteStatus.FAILED
                test_plan_status_table_obj.executeStatus = ExecuteStatus.FAILED
                raise Exception(f"测试任务{test_job.jobName}执行失败！！！")
            elif test_job.runFailedIsNeedContinue is True and self.execute_result["ret"] != 0:
                test_job_status_table_obj.executeStatus = ExecuteStatus.FAILED
                test_plan_status_table_obj.executeStatus = ExecuteStatus.FAILED
                logger.warning(f"测试任务{test_job.jobName}执行失败，继续执行下一个任务......")
            else:
                test_job_status_table_obj.executeStatus = ExecuteStatus.SUCCESS
                test_plan_status_table_obj.executeStatus = ExecuteStatus.SUCCESS
                logger.info(f"测试任务{test_job.jobName}执行成功")
            for test_step in test_job.testSteps:
                test_step_status_table_obj = TestStepStatusTable(
                    stepName=test_step.stepName,
                    id=test_step.id,
                    executeStatus=test_job_status_table_obj.executeStatus,
                    updateTime=datetime.datetime.now(),
                    createTime=datetime.datetime.now(),
                    processPid="11"
                )
                test_job_status_table_obj.testStepStatusList.append(test_step_status_table_obj)

            test_plan_status_table_obj.testJobStatusList.append(test_job_status_table_obj)

    def stop_test_plan(self, plan_id: str):
        # TODO 通过processPid进行进程kill
        ...

    def stop_test_job(self, job_id: str):
        ...

    def check_job_status(self, check_interval: int = 10):
        # TODO 执行任务后，开启一个异步线程，进行监听任务状态，如果任务处于运行中，修改executeStatus为running，如果任务结束，主动结束该子线程
        # 如果是本机执行，只需要检查是否存在进程即可，如果是非本机执行，需要使用ssh，然后检查进程是否存在
        # TODO 如果管控僵尸进程
        logger.info(f"开启监控线程，检查job时间间隔为{check_interval}")
        ...

    def distribute_script(self):
        # TODO 分发测试脚本到不同机器
        # 打包 -> 分发 -> 解压
        ...

    def get_test_job_list(self, plan_id: str = None):
        if plan_id is not None:
            test_job_list = [test_job.__repr__() for test_job in
                             self.sqlSession.query(TestJobTable).filter(TestJobTable.planId == plan_id).all()]
        else:
            test_job_list = [test_job.__repr__() for test_job in
                             self.sqlSession.query(TestJobTable).filter().all()]
        logger.info(test_job_list)
        return test_job_list

    def get_test_step_list(self, job_id: str = None):
        if job_id is not None:
            test_step_list = [test_job.__repr__() for test_job in
                              self.sqlSession.query(TestStepTable).filter(TestStepTable.jobId == job_id).all()]
        else:
            test_step_list = [test_job.__repr__() for test_job in
                              self.sqlSession.query(TestStepTable).filter().all()]
        logger.info(test_step_list)
        return test_step_list

    def get_test_job(self, job_id: str):
        test_job = self.sqlSession.query(TestJobTable).filter(TestJobTable.jobId == job_id).first()
        return test_job

    def get_test_job_status_list(self, plan_status_id: str = None):
        if plan_status_id is not None:
            test_job_status_list = [test_job.__repr__() for test_job in
                                    self.sqlSession.query(TestJobStatusTable).filter(
                                        TestJobStatusTable.id == plan_status_id).all()]
        else:
            test_job_status_list = [test_job.__repr__() for test_job in
                                    self.sqlSession.query(TestJobStatusTable).filter().all()]
        logger.info(test_job_status_list)
        return test_job_status_list

    def get_test_step_status_list(self, job_status_id: str = None):
        if job_status_id is not None:
            test_step_status_list = [test_job.__repr__() for test_job in
                                     self.sqlSession.query(TestStepStatusTable).filter(
                                         TestJobStatusTable.id == job_status_id).all()]
        else:
            test_step_status_list = [test_job.__repr__() for test_job in
                                     self.sqlSession.query(TestStepStatusTable).filter().all()]
        logger.info(test_step_status_list)
        return test_step_status_list
