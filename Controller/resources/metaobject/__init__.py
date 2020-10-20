from flask import Blueprint
from flask_restful import Api

from Common.utils.output import output_json
from Controller.resources.metaobject.metaobject import *

metaobject_bp = Blueprint('metaobject', __name__)
metaobject_api = Api(metaobject_bp, catch_all_404s=True)
metaobject_api.representation('application/json')(output_json)

metaobject_api.add_resource(MetaObjectListResource, '/metaobjectlist',endpoint='metaobjectlist')

metaobject_api.add_resource(MetaObjectResource, '/metaobject',endpoint='metaobject')

metaobject_api.add_resource(MetaFieldResource, '/metafield',endpoint='metafield')

