from functools import wraps

from flask import abort
from flask_jwt import current_identity


def list_user_permission(permissions):
    """
    返回序列化的权限
    :param permissions:{table_name:[...permissions...]}
    :return:[....]
    """
    return set([item for items in permissions.values() for item in items])


def perms(*permissions):
    """
    ModelName.Permission.[create/delete/select/alert]
    :param permissions: get_permission(User, Permission.Create), get_permission(User, Permission.Delete),
    :return: filter not permission
    """

    def decorator(f):
        @wraps(f)
        #  @wraps(view_func)的作用:
        # 不改变使用装饰器原有函数的结构(如__name__, __doc__)
        # 　wraps: print(f.__name__)  >>> f
        # 　print(f.__name__)  >>> decorated_function
        def decorated_function(*args, **kwargs):
            if not set(permission[0] for permission in permissions).issubset(current_identity['permissions']):
                return abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
