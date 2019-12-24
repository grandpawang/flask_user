from datetime import datetime

from flask import request, jsonify, Blueprint
from flask_jwt import jwt_required, current_identity

from app import get_config
from app.utils import common
from .. import User
from app.utils.model import form_to_model, quert2dict

cfg = get_config()
authManage = Blueprint('authManage', __name__)


# 用户登录接口已由flask-jwt默认定义好，默认路由是"/auth"，可以在配置文件中配置:
# JWT_AUTH_URL_RULE = '/login' 修改登录接口路由为'/login'
# 需要注意的是，登录接口的传值要使用 application/json 形式 post请求


# 获取个人信息 包括当前权限信息
@authManage.route('/current_user_permission')
@jwt_required()
def current_user_permission():
    return jsonify(common.trueReturn(dict(current_identity), 'success to get current user info'))


# 获取用于显示的个人信息
@authManage.route('/current_user')
@jwt_required()
def current_user():
    query = User.query.filter(User.id == current_identity['id']).all()
    return jsonify(common.trueReturn(quert2dict(query)[0], 'success to get current user info'))


# 注册
@authManage.route('/register', methods=['POST'])
def register():
    data = request.json
    register_user = User()
    form_to_model(data, register_user)
    register_user.status = True
    register_user.create_at = datetime.now()
    register_user.update_at = datetime.now()
    if register_user.save():
        return jsonify(common.trueReturn(request.form, '用户注册成功'))
    else:
        return jsonify(common.falseReturn(request.form, '用户注册失败'))


# 错误403 无权访问
@authManage.app_errorhandler(403)
def page_not_found(e):
    return jsonify(common.falseReturn('', 'power is\'t enough'))


# 错误404 不存在
@authManage.app_errorhandler(404)
def page_not_found(e):
    return jsonify(common.falseReturn('', "page_not_found"))


# 错误500 服务器错误
@authManage.app_errorhandler(500)
def internal_server_error(e):
    return jsonify(common.falseReturn('', "internal_server_error"))
