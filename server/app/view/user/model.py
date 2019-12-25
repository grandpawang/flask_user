from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from database.MainModel import MainModel

user_permission = db.Table(
    'user_permission',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), comment='用户编号'),
    db.Column('permission_id', db.Integer, db.ForeignKey(
        'permission.id', ondelete='CASCADE'), comment='操作权限编号'),
    comment='用户操作权限',
)

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), comment='用户编号'),
    db.Column('role_id', db.Integer, db.ForeignKey(
        'role.id', ondelete='CASCADE'), comment='角色编号'),
    comment='用户角色',
)


# 用户管理
class User(db.Model, MainModel):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户'}
    # __permission__ = {}
    username = db.Column(db.String(20), unique=True,
                         nullable=False, comment='用户名', )
    password_hash = db.Column(db.String(255), nullable=False, comment='密码')
    fullname = db.Column(db.String(40), nullable=False, comment='真实姓名', )
    phone = db.Column(db.String(11), nullable=False, comment='电话', )
    create_at = db.Column(db.DateTime(), nullable=False, comment='创建时间', )
    update_at = db.Column(db.DateTime(), nullable=False, comment='更新时间', )
    status = db.Column(db.Boolean(), nullable=False, comment='账户状态', )
    head_img = db.Column(db.LargeBinary(65536), nullable=True, comment="头像", )  # max16M
    # LargeBinary(16777216)	longblob	str	二进制，max32M

    permissions = db.relationship(
        'Permission', secondary=user_permission)  # 操作权限
    roles = db.relationship('Role', secondary=user_role)  # 角色

    @property
    def password(self):
        raise AttributeError("password can't to read!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # 哈希对比
        """
        对比密码
        :param hash: 哈希密码
        :param password: 要与哈希比较的纯文本密码。
        :return:
        """
        return check_password_hash(self.password_hash, password)


# 用户角色管理
role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey(
        'role.id', ondelete='CASCADE'), comment='角色编号'),
    db.Column('permission_id', db.Integer, db.ForeignKey(
        'permission.id', ondelete='CASCADE'), comment='操作权限编号'),
    comment='角色操作权限',
)

# 机构权限管理
group_permission = db.Table(
    'group_permission',
    db.Column('group_id', db.Integer, db.ForeignKey(
        'group.id', ondelete='CASCADE'), comment='机构编号'),
    db.Column('permission_id', db.Integer, db.ForeignKey(
        'permission.id', ondelete='CASCADE'), comment='操作权限编号'),
    comment='角色操作权限',
)


# 机构表
# 一个角色一个机构
class Group(db.Model, MainModel):
    __tablename__ = 'group'
    __table_args__ = {'comment': '机构'}
    comment = db.Column(db.String(50), unique=True,
                        nullable=False, comment='注释', )
    # 一对多
    roles = db.relationship('Role', cascade='all, delete-orphan', back_populates='group')  # 角色
    # 多对多
    permissions = db.relationship('Permission', secondary=group_permission, )


# 角色管理
class Role(db.Model, MainModel):
    __tablename__ = 'role'
    __table_args__ = {'comment': '角色'}
    comment = db.Column(db.String(50), unique=True,
                        nullable=False, comment='注释', )
    group_id = db.Column(db.Integer, db.ForeignKey(
        'group.id', ondelete='CASCADE'), comment='机构编号')
    # one-way_many_to_many
    # secondary 关联表表名
    # back_populates (权限反过来找到角色)可以访问角色对应的所有权限
    # cascade='all, delete-orphan' 一对多 一的那个被删除 多的也一起被删除
    permissions = db.relationship(
        'Permission', secondary=role_permission, )  # 操作权限

    group = db.relationship('Group', back_populates="roles")
