from database import db
from database.SupportModel import SupportModel


class Permission(db.Model, SupportModel):
    __tablename__ = 'permission'
    __table_args__ = {'comment': '操作权限'}
    permission = db.Column(db.String(50), nullable=False, comment='权限编号')
    comment = db.Column(db.String(50), nullable=False, comment='备注')
