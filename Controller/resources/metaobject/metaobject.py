from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request, g, current_app
from sqlalchemy.orm import load_only, contains_eager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import insert
from flask_restful import inputs
from Common.metadatas import db
from Common.metadatas.metaobject import MetaObject,MetaField
from Common.utils import parser


class MetaObjectListResource(Resource):

    def get(self):
        MetaObjectList = MetaObject.query.all()
        result = []
        for obj in MetaObjectList:
            result.append(dict(
                id = obj.id,
                name = obj.name,
                label = obj.label
            ))
        return result


class MetaObjectResource(Resource):

    def get(self):
        json_parser = RequestParser()
        json_parser.add_argument('name', required=True, location='json')
        args = json_parser.parse_args()

        obj = MetaObject.query.filter_by(name=args.name).first()
        if obj is None:
            return

        result = {
            'id': obj.id,
            'name': obj.name,
            'label': obj.label
        }
        return result

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('label', location='json')
        json_parser.add_argument('description', location='json')
        args = json_parser.parse_args()
        name = args.name
        label = args.label
        description = args.description
        obj = MetaObject(
            id = current_app.id_worker.get_id(),
            name = name,
            label = label,
            description = description,
            createby = 10000,
            modifiedby = 10000
        )
        db.session.add(obj)
        db.session.commit()

        return 'ok'


class MetaFieldListResource(Resource):

    def get(self):
        MetaFieldList = MetaField.query.all()
        result = []
        for obj in MetaFieldList:
            result.append(dict(
                id = obj.id,
                name = obj.name,
                label = obj.label
            ))
        return result


class MetaFieldResource(Resource):

    def get(self):
        json_parser = RequestParser()
        json_parser.add_argument('objectname', required=True, location='json')
        args = json_parser.parse_args()

        obj = MetaObject.query.filter_by(name=args.objectname).first()
        if obj is None:
            return '无此对象'

        fields = MetaField.query.filter_by(fk_metaobject_id = obj.id).all()
        result = []
        for field in fields:
            result.append(dict(
                id=field.id,
                name=field.name,
                label=field.label
            ))
        return result

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('objectname', required=True, location='json')
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('label', location='json')
        json_parser.add_argument('description', location='json')
        args = json_parser.parse_args()
        obj = MetaObject.query.filter_by(name=args.objectname).first()
        if obj is None:
            return '无此对象'

        fk_metaobject_id = obj.id
        name = args.name
        label = args.label
        description = args.description
        obj = MetaField(
            id = current_app.id_worker.get_id(),
            fk_metaobject_id = fk_metaobject_id,
            name = name,
            label = label,
            description = description,
            createby = 10000,
            modifiedby = 10000
        )
        db.session.add(obj)
        db.session.commit()

        return 'ok'

