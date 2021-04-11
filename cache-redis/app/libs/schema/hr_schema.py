from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters


class DepartmentGetAllParams(Parameters):
    isReloadCache = base_fields.Boolean()
