from . import db


class SupportModel:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='编号')

    def __repr__(self):
        return self.id

    def __init__(self, *args, **kwargs):
        pass

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

