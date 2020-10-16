from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request, g, current_app
from sqlalchemy.orm import load_only, contains_eager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import insert
from flask_restful import inputs
from Common.metadatas import db
from Common.metadatas.user import User
from Common.utils import parser


class UserListResource(Resource):

    def get(self):
        userList = User.query.all()
        result = []
        for user in userList:
            result.append(dict(
                id = user.id,
                name = user.name,
                mobile = user.mobile
            ))
        return {'userList': result}


class UserResource(Resource):

    def get(self):
        json_parser = RequestParser()
        json_parser.add_argument('mobile', action='append', type=inputs.positive, required=True, location='json')
        args = json_parser.parse_args()

        user = User.query.filter_by(mobile=args.mobile).first()
        result = {
            'id' : user.id,
            'name':  user.name,
            'mobile':  user.mobile
        }
        return {'userinfo': result}

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('mobile', type=parser.mobile, required=True,location='json') #required=True,
        json_parser.add_argument('name', required=True,location='json')
        args = json_parser.parse_args()
        mobile = args.mobile
        name = args.name
        userinfo = User(mobile=mobile, name=name)
        db.session.add(userinfo)
        db.session.commit()

        return 'ok'

    # def delete(self):
    #     """
    #     删除指定用户频道
    #     """
    #     user_id = g.user_id
    #     UserChannel.query.filter_by(user_id=user_id, channel_id=target).update({'is_deleted': True})
    #     db.session.commit()
    #
    #     # 清除缓存
    #     cache_channel.UserChannelsCache(user_id).clear()
    #
    #     return {'message': 'OK'}, 204
