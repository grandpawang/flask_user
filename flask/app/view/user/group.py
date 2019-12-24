from flask import jsonify, Blueprint
from flask_jwt import jwt_required

from app.utils import common
from app.view.auth.model import Permission
from app.view.user.model import Group, Role
from app.permission.authorization import perms
from app.utils.model import common_list, common_delete, common_edit

groupManage = Blueprint('groupManage', __name__)


# 查
@groupManage.route('/group_list', methods=['POST', 'GET'])
@jwt_required()
@perms(Group.Permission.select, )
def group_list():
    query = common_list(Group)
    return jsonify(common.trueReturn(query, 'success to list data'))


# 删
@groupManage.route('/group_delete')
@jwt_required()
@perms(Group.Permission.delete, )
def group_delete():
    query = common_delete(Group)
    if query:
        return jsonify(common.trueReturn('', 'success to delete data'))
    else:
        return jsonify(common.falseReturn('', 'fail to delete data'))


# 改
@groupManage.route('/group_edit', methods=['POST'])
@jwt_required()
@perms(Group.Permission.alert, )
def group_edit():
    def edit_model(form, model):
        setattr(model, "permissions",
                [Permission.query.filter(Permission.id == permission).first() for permission in form['permissions']])
        setattr(model, "roles",
                [Role.query.filter(Role.id == role).first() for role in form['roles']])
    query = common_edit(Group, edit_model=edit_model)
    if query:
        return jsonify(common.trueReturn('', 'success to alert data'))
    else:
        return jsonify(common.falseReturn('', 'fail to alert data'))

