from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request, g, current_app
from sqlalchemy.orm import load_only, contains_eager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import insert
from flask_restful import inputs
from Common.metadatas import db
from Common.metadatas.metaobject import MetaObject,MetaField
from Common.models.datahandler import Handler
from Common.utils import parser
import json


class DataResource(Resource):
        
    def post(self):
        '''
            1.check对象是否存在
            2.根据对象获取字段
        '''
        
        json_parser = RequestParser()
        json_parser.add_argument('metaobjectname', required=True, location='json')
        json_parser.add_argument('method', required=True, location='json')
        json_parser.add_argument('data', required=True, location='json')     
        json_parser.add_argument('objectid', location='json')           
        args = json_parser.parse_args()
        
        obj = MetaObject.query.filter_by(name=args.metaobjectname).first()
        if obj == None: return '对象不存在'
                
        fields = MetaField.query.filter_by(fk_metaobject_id=obj.id).all()
        if fields == None: return '字段集不存在'
        
        dataresult = json.dumps(args.data)
        
        if args.method == 'add':
            #新增
            Handler.insert(args.metaobjectname, dataresult)
            
        else:
            #编辑
            Handler.update(args.metaobjectname, args.objectid, dataresult)

        return 'ok'

class DataListResource(Resource):

    def post(self):
        '''
            1.check对象是否存在
            2.根据条件进行搜索
        '''
        
        json_parser = RequestParser()
        json_parser.add_argument('metaobjectname', required=True, location='json')
        json_parser.add_argument('condition', location='json')
        json_parser.add_argument('orderby', location='json')   
        json_parser.add_argument('pagesize', location='json')     
        json_parser.add_argument('pageno', location='json')             
        json_parser.add_argument('objectid', location='json')           
        args = json_parser.parse_args()
        
        obj = MetaObject.query.filter_by(name=args.metaobjectname).first()
        if obj == None: return '对象不存在'
                
        fields = MetaField.query.filter_by(fk_metaobject_id=obj.id).all()
        if fields == None: return '字段集不存在'
        
        fieldname_list = [_ for i.name in fields]
        query_result = Handler.query_page(args.metaobjectname, fieldname_list, args.condition, args.orderby, args.pagesize, args.pageno)
        
        return query_result

