from database.utils import DictObj
from . import db


class MainModel:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='编号')

    def __repr__(self):
        return self.id

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def initPermissions(cls):
        for obj in cls.__subclasses__():
            try:  # 初始化类的权限
                table_name = getattr(obj, '__tablename__', '')
                table_comment = getattr(obj, '__table_args__', {}).get('comment')
                permission = getattr(obj, '__permission__', {})
                permission.update({  # 初始化 四个权限 增删查改
                    'create': (f'{table_name}.create', f'增加{table_comment}'),
                    'delete': (f'{table_name}.delete', f'删除{table_comment}'),
                    'alert': (f'{table_name}.alert', f'修改{table_comment}'),
                    'select': (f'{table_name}.select', f'查询{table_comment}')
                })
                setattr(obj, 'Permission', DictObj(permission))
            except Exception as e:
                print(e)

    def save(self):
        try:
            db.session.add(self)  # self实例化对象代表就是u对象
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    # 定义静态类方法接收List参数
    @staticmethod
    def save_all(List):
        try:
            db.session.add_all(List)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    # 定义删除方法
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
