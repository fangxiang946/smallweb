from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request, g, current_app
from sqlalchemy.orm import load_only, contains_eager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import insert
from flask_restful import inputs
from Common.metadatas import db
from Common.metadatas.metaobject import MetaObject, MetaField
from Common.models.datahandler import Handler
from Common.utils import parser
import json
import ast

class DataResource(Resource):

    def get(self):
        '''
            1.check对象是否存在
            2.根据条件进行搜索
        '''

        json_parser = RequestParser()
        json_parser.add_argument('objectname', required=True, location='json')
        json_parser.add_argument('condition', location='json')
        json_parser.add_argument('orderby', location='json')
        json_parser.add_argument('pagesize', location='json')
        json_parser.add_argument('pageno', location='json')
        json_parser.add_argument('objectid', location='json')
        args = json_parser.parse_args()

        obj = MetaObject.query.filter_by(name=args.objectname).first()
        if obj is None:
            return '对象不存在'

        fields = MetaField.query.filter_by(fk_metaobject_id=obj.id).all()
        if fields is None:
            return '字段集不存在'
        condition = None if args.condition is None else ast.literal_eval(args.condition)
        fieldname_list = [i.name for i in fields]
        query_result = Handler.query_page(args.objectname, fieldname_list, condition, args.orderby,
                                          args.pagesize, args.pageno)
        return query_result

    def post(self):
        '''
            1.check对象是否存在
            2.根据对象获取字段
        '''
        
        json_parser = RequestParser()
        json_parser.add_argument('objectname', required=True, location='json')
        json_parser.add_argument('method', required=True, location='json')
        json_parser.add_argument('data', required=True, location='json')
        json_parser.add_argument('condition', location='json')
        args = json_parser.parse_args()
        
        obj = MetaObject.query.filter_by(name=args.objectname).first()
        if obj is None:
            return '对象不存在'
                
        fields = MetaField.query.filter_by(fk_metaobject_id=obj.id).all()
        if fields is None:
            return '字段集不存在'
        
        data = ast.literal_eval(args.data) #转成字典
        if args.method == 'add':
            #新增
            if isinstance(data, dict):
                data.update({"_id": current_app.id_worker.get_id()})
            elif isinstance(data, list) or isinstance(data, tuple):
                for i in data:
                    if isinstance(i, dict):
                        i.update({"_id": current_app.id_worker.get_id()})
            Handler.insert(args.objectname, data)
        elif args.method == 'createUpdate':
            #整体更新
            Handler.update(args.objectname, data)
        elif args.method == 'update' and args.condition is not None:
            #指定条件和结果更新
            condition = ast.literal_eval(args.condition)  # 转成字典
            Handler.update(args.objectname, condition, data)
        return 'ok'

    def delete(self):
        json_parser = RequestParser()
        json_parser.add_argument('objectname', required=True, location='json')
        json_parser.add_argument('condition', location='json')
        args = json_parser.parse_args()

        obj = MetaObject.query.filter_by(name=args.objectname).first()
        if obj is None:
            return '对象不存在'

        condition = {} if args.condition is None else ast.literal_eval(args.condition)
        result = Handler.delete(args.objectname, condition)
        return {"result":result}


