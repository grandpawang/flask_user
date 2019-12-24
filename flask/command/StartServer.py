from flask_script import Server
from app import register_blueprinter


class StartServer(Server):
    def run(self):
        pass

    def __init__(self, app, *args, **kwargs):
        register_blueprinter(app)
        super().__init__(*args, **kwargs)
