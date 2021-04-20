import json
import logging
from datetime import datetime
from .celery_app import celery
from .back_ground.common_task import CommonTask
from .back_ground.notice_task import EmailNotice
from .back_ground.hr_task.employee_task import EmployeeTask
from .back_ground.cache.hr_cache_task import HRCacheTask

logger = logging.getLogger(__name__)

common_task = CommonTask(celery.conf)
email_notice = EmailNotice(celery.conf)
employee_task = EmployeeTask(celery.conf)
hr_cache_task = HRCacheTask(celery.conf)


@celery.task(name='daily_health_check')
def daily_health_check():
    common_task.do_health_check()
    return "daily_health_check"


@celery.task(name='write_hello')
def write_hello():
    """
    write something to logs file for start
    """
    try:
        logger.info("Hello from celery task at {}. Ready for run!".format(str(datetime.now())))
    except Exception as ex:
        logger.error("write_hello task fail " + str(ex.__str__()))


@celery.task(name='auto_check_hire_date')
def auto_check_hire_date():
    """
    auto connect to database and get all use have hire_date is today.
    send list of staff to special email
    """
    try:
        list_employee = employee_task.action_with_hire_date()
        if list_employee:
            celery.send_task("send_birthday_email", args=[list_employee])

    except Exception as ex:
        logger.error("auto_check_hire_date task fail " + str(ex.__str__()))


@celery.task(name='send_birthday_email')
def send_birthday_email(list_employee: list):
    """
    auto connect to database and get all use have hire_date is today.
    send list of staff to special email
    """
    try:
        list_email = [employee['EMAIL'] for employee in list_employee]
        email_notice.send_welcome_day_email_to_employee(list_email)
        logger.info("send_birthday_email DONE")
    except Exception as ex:
        logger.error("send_birthday_email task fail " + str(ex.__str__()))


@celery.task(name='reload_department_cache')
def reload_department_cache():
    """
    auto reload cache by cron-job

    """
    try:
        result = hr_cache_task.reload_department_cache()
        logger.info("reload_department_cache result: {}".format(json.dumps(result)))
    except Exception as ex:
        logger.error("reload_department_cache task fail " + str(ex.__str__()))


@celery.task(name='get_departments')
def get_departments():
    """
    get all department from cache or database

    """
    try:
        result = hr_cache_task.get_derpartment()
        logger.info("get_departments result: {}".format(json.dumps(result)))
    except Exception as ex:
        logger.error("get_departments task fail " + str(ex.__str__()))