from app import create_app
from command import manager

app = create_app()
manager = manager(app)

if __name__ == '__main__':
    manager.run()
