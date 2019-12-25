import os

from flask import Flask, make_response
from flask_cors import CORS
from flask_jwt import JWT
from flask_migrate import Migrate

from app.view import *

from database.MainModel import MainModel
from app.config import config


def get_basedir():
	return os.path.abspath(os.path.dirname(__file__))


def get_config():
	return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app():
	config = get_config()
	app = Flask(__name__)
	app.config.from_object(config)
	config.init_app(app)
	db.init_app(app)
	Migrate(app, db)
	CORS(app, supports_credentials=True)
	MainModel.initPermissions()

	@app.after_request
	def af_request(resp):
		"""
		请求钩子，在所有的请求发生后执行，加入headers。
		:param resp:
		:return:
		"""
		resp = make_response(resp)
		resp.headers['Access-Control-Allow-Origin'] = '*'
		resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE'
		resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, ' \
													   'Accept, Authorization'
		return resp

	return app


def register_blueprinter(app):
	from app.permission.authenticate import authenticate, identity
	from app.view.auth.views import authManage
	from app.view.user.user import userManage
	from app.view.user.role import roleManage
	from app.view.user.group import groupManage

	JWT(app, authenticate, identity)
	app.register_blueprint(authManage)
	app.register_blueprint(userManage)
	app.register_blueprint(roleManage)
	app.register_blueprint(groupManage)
