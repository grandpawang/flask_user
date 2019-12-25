from flask import jsonify, Blueprint
from flask_jwt import jwt_required

from app.utils import common
from app.view.auth.model import Permission
from app.view.user.model import Role
from app.permission.authorization import perms
from app.utils.model import common_list, common_delete, common_edit

roleManage = Blueprint('roleManage', __name__)


# 查
@roleManage.route('/role_list', methods=['POST', 'GET'])
@jwt_required()
@perms(Role.Permission.select, )
def role_list():
    query = common_list(Role)
    return jsonify(common.trueReturn(query, 'success to list data'))


# 删
@roleManage.route('/role_delete')
@jwt_required()
@perms(Role.Permission.delete, )
def role_delete():
    query = common_delete(Role)
    if query:
        return jsonify(common.trueReturn('', 'success to delete data'))
    else:
        return jsonify(common.falseReturn('', 'fail to delete data'))


# 改
@roleManage.route('/role_edit', methods=['POST'])
@jwt_required()
@perms(Role.Permission.alert, )
def role_edit():
    def edit_model(form, model):
        setattr(model, "permissions",
                [Permission.query.filter(Permission.id == permission).first() for permission in form['permissions']])
    query = common_edit(Role, edit_model=edit_model)
    if query:
        return jsonify(common.trueReturn('', 'success to alert data'))
    else:
        return jsonify(common.falseReturn('', 'fail to alert data'))

