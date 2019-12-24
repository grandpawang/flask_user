from datetime import datetime

from flask import jsonify, Blueprint
from flask_jwt import jwt_required, current_identity

from app.permission.authorization import perms
from app.utils import common
from app.view.auth.model import Permission
from app.view.user.model import User, Role
from app.utils.model import common_list, common_delete, common_edit

userManage = Blueprint('userManage', __name__)

# # 头像文件上传
# @userManage.route('/user_upload', methods=['POST'])
# @jwt_required()
# @perms(User.Permission.alert)
# def user_upload():
#     file = request.files['file']
#     file_path = os.path.join(upload_folder, f'{current_identity["username"]}_{current_identity["fullname"]}')
#     if file:
#         if not os.path.exists(file_path):  # 不存在文件则创建
#             os.mkdir(file_path)
#         file.save(os.path.join(file_path, 'head_img.jpg'))
#     return jsonify(common.trueReturn("ok", "success to upload file"))


# 查
@userManage.route('/user_list', methods=['POST', 'GET'])
@jwt_required()
@perms(User.Permission.select, )
def user_list():
    query = common_list(User, filter_select=User.id !=
                        current_identity['id'])  # 不显示自己的信息
    return jsonify(common.trueReturn(query, 'success to list data'))


# 删
@userManage.route('/user_delete')
@jwt_required()
@perms(User.Permission.delete, )
def user_delete():
    query = common_delete(User)
    if query:
        return jsonify(common.trueReturn('', 'success to delete data'))
    else:
        return jsonify(common.falseReturn('', 'fail to delete data'))


# 改
@userManage.route('/user_edit', methods=['POST'])
@jwt_required()
@perms(User.Permission.alert, )
def user_edit():
    def edit_model(form, model):
        setattr(model, "update_at", datetime.now())
        setattr(model, "permissions",
                [Permission.query.filter(Permission.id == permission).first() for permission in form['permissions']])
        setattr(model, "roles",
                [Role.query.filter(Role.id == role).first() for role in form['roles']])

        if not model.create_at:  # 新增用户
            setattr(model, "create_at", datetime.now())
            model.password = "1234"
        if form['head_img']:
            setattr(model, "head_img", form['head_img'].encode())
        else:
            setattr(model, "head_img", None)

    query = common_edit(User, edit_model=edit_model)
    if query:
        return jsonify(common.trueReturn('', 'success to alert data'))
    else:
        return jsonify(common.falseReturn('', 'fail to alert data'))
