from app.view.user.model import User


def error_handler(e):
    print(e)
    return 'something bad happened', 400


def authenticate(username, password):
    login_user = User.query.filter(User.username == username).first()
    if login_user is None:
        error_handler('cant to find user')
    else:
        if login_user.check_password(password) and login_user.status:
            return login_user
        else:
            error_handler('password error')


def identity(payload):
    id = payload['identity']
    user_data = User.query.filter(User.id == id).first()
    # 这里一定要copy 不然回修改user的permission值
    permissions = user_data.permissions.copy()

    for role in user_data.roles:
        permissions += role.permissions.copy() + role.group.permissions.copy()

    permissions = [permission.permission for permission in list(set(permissions))]
    return {
        'id': user_data.id,
        'permissions': permissions,
    }
