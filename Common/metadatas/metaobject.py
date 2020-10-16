from . import db
from datetime import datetime

class MetaObject(db.Model):
    """
    元数据对象
    """
    __tablename__ = 'MetaObject'

    id = db.Column('id', db.Integer, primary_key=True, doc='对象ID')
    name = db.Column(db.String, doc='名称')
    label = db.Column(db.String, doc='简称')
    description = db.Column(db.String, doc='描述')
    ispublic = db.Column(db.Boolean, default=True, doc='状态，是否发布')
    createby = db.Column(db.String, doc='创建人ID')
    modifiedby = db.Column(db.String, doc='修改人ID')
    createtime = db.Column(db.DateTime, default=datetime.now, doc='创建时间')
    updatetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

    Field = db.relationship('MetaField',uselist=True)

class MetaField(db.Model):
    """
    元数据字段
    """
    __tablename__ = 'MetaField'

    id = db.Column('id', db.Integer, primary_key=True, doc='字段ID')
    fk_metaobject_id = db.Column(db.Integer, db.ForeignKey('MetaObject.id'), doc='对象ID')
    name = db.Column(db.String, doc='名称')
    label = db.Column(db.String, doc='简称')
    description = db.Column(db.String, doc='描述')
    createby = db.Column(db.String, doc='创建人ID')
    modifiedby = db.Column(db.String, doc='修改人ID')
    createtime = db.Column(db.DateTime, default=datetime.now, doc='创建时间')
    updatetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
