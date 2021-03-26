from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from api import *
from app import create_app
from flask_cors import CORS

app = create_app('develope')
CORS(app, supports_credentials=True)
manager = Manager(app)
# Migrate(app, db)
# manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    app.run(port=9050,debug=True)