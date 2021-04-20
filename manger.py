from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from api import *
from app import create_app
from flask_cors import CORS
from proxy_pool.helper.scheduler import runScheduler


app = create_app('develope')
# app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
CORS(app, supports_credentials=True,resources=r'/*')
manager = Manager(app)
# Migrate(app, db)
# manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    app.run(port=9050,host='0.0.0.0',debug=True)
