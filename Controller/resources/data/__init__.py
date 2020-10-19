from flask import Blueprint
from flask_restful import Api

from Common.utils.output import output_json
from Controller.resources.data.dataobject import *

data_bp = Blueprint('dataobject', __name__)
data_api = Api(data_bp, catch_all_404s=True)
data_api.representation('application/json')(output_json)

data_api.add_resource(DataListResource, '/datalist',endpoint='datalist')

data_api.add_resource(DataResource, '/data',endpoint='data')
