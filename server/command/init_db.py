from datetime import datetime

from flask_script import Command


# 初始化数据库命令init_db
class InitDataBase(Command):
    def run(self):
        from app.view.user.model import User, Group, Role
        from app.view.auth.model import Permission
        from database.MainModel import MainModel

        permissions = []
        for model in MainModel.__subclasses__():
            permissions += model.Permission.map.values()

        # 删除所有权限
        for permission in Permission.query.all():
            permission.delete()

        # 删除所有机构
        for group in Group.query.all():
            group.delete()

        # 删除所有角色
        for role in Role.query.all():
            role.delete()

        # 删除所有用户
        for user in User.query.all():
            user.delete()

        group1 = Group(id=1, comment='管理')
        group2 = Group(id=2, comment='用户')

        role = Role(id=1, comment='管理员', group=group1)
        role.permissions = [Permission(permission=permission, comment=comment) for permission, comment in permissions]
        group1.roles = [role]
        role.save()
        group1.save()

        role2 = Role(id=2, comment='普通用户',  group=group2)
        role2.permissions = []
        group2.roles = [role2]
        role2.save()
        group2.save()

        user = User()
        user.username = "wang"
        user.fullname = "王大爷"
        user.password = "1234"
        user.phone = "17324075315"
        user.status = True
        user.create_at = datetime.now()
        user.update_at = datetime.now()
        user.permissions = [Permission(permission="test.test", comment="test")]
        user.roles = [role, ]
        user.save()

        user = User()
        user.username = "wang2"
        user.fullname = "王大爷2"
        user.password = "1234"
        user.phone = "17324075314"
        user.status = True
        user.create_at = datetime.now()
        user.update_at = datetime.now()
        user.roles = [role2, ]
        user.permissions = [Permission(permission="test2.test2", comment="test2")]
        user.save()

