import json
from .cache_task import CommonCacheTask
from celery.utils.log import get_task_logger
from app.task.back_ground.models.department_controller import DepartmentController

logger = get_task_logger(__name__)


class HRCacheTask(CommonCacheTask):
    def __init__(self, config):
        super().__init__(config)
        self.sqlalchemy_database_uri = self.config['SQLALCHEMY_DATABASE_URI']

    def get_derpartment(self):
        try:
            key_cache = self.config.get('CACHE_DEPARTMENT_KEY', "")
            value = self.get_from_cache(key_cache)
            if value:
                return json.loads(value)
            else:
                return self.reload_department_cache()
        except Exception as ex:
            logger.warning("get_derpartment {}".format(ex.__str__()))
            return self.reload_department_cache()

    def reload_department_cache(self):
        try:
            key_cache = self.config.get('CACHE_DEPARTMENT_KEY', "")
            data = self.get_departments_from_database()
            return self.save_to_cache(key_cache, data)
        except Exception as ex:
            logger.warning("reload_department_cache {}".format(ex.__str__()))
            return None

    def get_departments_from_database(self):
        db_ctrl = DepartmentController(self.sqlalchemy_database_uri)
        try:
            offset = 0
            limit = 20
            list_deparment= []
            while True:
                try:
                    result = db_ctrl.get_all_departments(offset, limit)
                except Exception as ex:
                    logger.warning(ex.__str__())
                    break
                if result:
                    list_deparment.extend(result)
                    offset += limit
                else:
                    break
            return list_deparment
        except Exception as ex:
            logger.warning("get_departments_from_database {}".format(ex.__str__()))
            return []
        finally:
            db_ctrl.close()
