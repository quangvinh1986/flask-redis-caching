from flask import current_app
from datetime import datetime
from werkzeug.exceptions import NotFound
from app.libs.schema import hr_schema
from flask_restplus_patched import Resource
from app.extensions import api
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import CustomControllerException, ERROR_MESSAGE
from app.libs.common import redis_lib
from app.database_connect import department_model


ns = api.namespace("hrApi")


@ns.route("/departments")
class DepartmentAPI(Resource):
    @ns.parameters(hr_schema.DepartmentGetAllParams())
    def get(self, args):
        """
        get all departments by cache or none
        :param args:
        :return:
        """
        try:
            is_reload_cache = args.get('isReloadCache', False)
            result = dict()
            is_get_new_data = False
            key_cache = current_app.config.get("CACHE_DEPARTMENT_KEY")

            if is_reload_cache:
                lst_departments = self.get_value_from_database()
                if lst_departments:
                    is_get_new_data = True
                    result['data'] = lst_departments
                else:
                    result = self.get_value_from_cache(key_cache)
            else:
                result = self.get_value_from_cache(key_cache)
                if not result:
                    lst_departments = self.get_value_from_database()
                    is_get_new_data = True
                    result['data'] = lst_departments

            if not result or not result["data"]:
                raise NotFound("Can't get department informations")

            if is_get_new_data and result["data"]:
                result["dateReceived"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                redis_lib.save_all_to_redis(result, key_cache)

            result["isCache"] = not is_get_new_data
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return {'error': trace.get_message(), 'status': "FAIL"}, 500

    def get_value_from_database(self):
        departments = department_model.get_all_records()
        if departments:
            return [department.get_json_serializeable() for department in departments]
        else:
            return []

    def get_value_from_cache(self, key_cache):
        return redis_lib.get_all_from_redis(key_cache)
