import logging
from app.extensions import db
from .models import Departments
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import CustomControllerException, OK_MESSAGE

logger = logging.getLogger(__name__)


# <editor-fold desc="DepartmentController">
class DepartmentController:
    def get_by_id(self, _id):
        """
        :param _id:
        :return:
        """
        result = Departments.query.filter(Departments.DEPARTMENT_ID == _id).first()
        if result:
            return result.get_json_serializeable()
        else:
            return None

    def add_or_update(self, params, _id=""):
        """add new if don't exist
            update if exist
        :param _id: id of record
        :param params: dictionary
        :return: content is dictionary {"content":"...."}
        """
        try:
            if _id and self.get_by_id(_id):
                return self.update(_id, params)
            else:
                return self.add(params)
        except Exception as ex:
            db.session.rollback()
            trace = TraceException("DepartmentsController: add_or_update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def add(self, args):
        """add new region
        :param args: dictionary for region params
        :return:
        """
        resend_case = Departments(**args)
        session = db.session()
        session.add(resend_case)
        try:
            session.commit()
            return OK_MESSAGE
        except Exception as e:
            trace = TraceException("DepartmentsController:", "insert DB fail", e.__str__())
            raise CustomControllerException(trace.get_message())
            # logger.warning(trace.get_message())
            # return {'error': trace.get_message(), 'status': "NOK"}

    def update(self, _id, args):
        """
        update by id
        :param
        :return:
        """
        db.session.query(Departments).filter_by(DEPARTMENT_ID=_id).update(args)
        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            trace = TraceException("DepartmentsController:", "update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def delete(self, _id):
        obj = Departments.query.filter(Departments.DEPARTMENT_ID == _id).first()
        if not obj:
            return OK_MESSAGE
        db.session.delete(obj)

        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            db.session.rollback()
            trace = TraceException("DepartmentsController:", "delete DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def multi_delete(self, list_id):
        session = db.session()
        try:
            delete_q = Departments.__table__.delete().where(Departments.DEPARTMENT_ID.in_(set(list_id)))
            session.execute(delete_q)
            session.commit()
            return OK_MESSAGE
        except Exception as ex:
            session.rollback()
            trace = TraceException("DepartmentsController: multi_delete " + ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_limit(self, limit):
        try:
            if limit:
                return db.session().query(Departments).order_by().limit(limit).all()
            else:
                return db.session().query(Departments).order_by().all()
        except Exception as ex:
            trace = TraceException("DepartmentsController:", "get_limit", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_all_records(self):
        try:
            return db.session().query(Departments).order_by().all()
        except Exception as ex:
            trace = TraceException("DepartmentsController:", "get_all_records", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_all_case(self, region_name="", limit=0):
        if region_name:
            return self.get_by_region_name(region_name, limit)
        return self.get_limit(limit)

    def get_by_region_name(self, department_name, limit=0):
        try:
            if limit:
                return db.session().query(Departments).filter(Departments.DEPARTMENT_NAME == department_name).order_by().limit(limit).all()
            else:
                return db.session().query(Departments).filter(Departments.DEPARTMENT_NAME == department_name).order_by().all()
        except Exception as ex:
            trace = TraceException("DepartmentsController:", "get_by_region_name", ex.__str__())
            raise CustomControllerException(trace.get_message())
# </editor-fold>