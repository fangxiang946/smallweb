from flask import Blueprint
from flask_restful import Api

# from . import passport
# from . import following, channel, blacklist, profile, figure
from Common.utils.output import output_json
from Controller.resources.user.UserController import UserListResource, UserResource

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp, catch_all_404s=True)
user_api.representation('application/json')(output_json)

user_api.add_resource(UserListResource, '/v1_0/userlist',endpoint='userlist')

user_api.add_resource(UserResource, '/v1_0/user',endpoint='user')
