from flask_migrate import MigrateCommand
from flask_script import Manager

from command.StartServer import StartServer
from command.init_db import InitDataBase


def manager(app):
    script_manager = Manager(app)
    script_manager.add_command('db', MigrateCommand)
    script_manager.add_command('init_db', InitDataBase)
    script_manager.add_command('run', StartServer(app, host='0.0.0.0', port=8000))
    return script_manager
