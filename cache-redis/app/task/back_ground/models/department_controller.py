from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime, Float, and_, func, extract
from . import DBConnection


class DepartmentController(DBConnection):

    def __init__(self, connection_string):
        DBConnection.__init__(self, connection_string)
        self.Employee = self.get_table()
        self.connection = self.db.connect()

    def get_table(self):
        table = Table('DEPARTMENTS', self.meta,
                      Column('DEPARTMENT_ID', Integer, primary_key=True),
                      Column('DEPARTMENT_NAME', String),
                      Column('MANAGER_ID', Integer),
                      Column('LOCATION_ID', Integer),
                      autoload=True, autoload_with=self.db
                      )
        return table

    def close(self):
        # self.session.close()
        self.connection.close()

    def get_all_departments(self, offset=0, limit=20):
        """
        :return list of dictionary (convert from row_proxy)
        example: [
                    {'DEPARTMENT_ID': 100, 'DEPARTMENT_NAME': 'STEVEN', 'MANAGER_ID': '100', ...},
                ]
        """
        select_statement = self.Employee.select() \
            .offset(offset).limit(limit)
        value = self.connection.execute(select_statement).fetchall()
        return [dict(row) for row in value]

