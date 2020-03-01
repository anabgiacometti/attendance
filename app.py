from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail


app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from views.login import *
from views.users import *
from views.system import *
from views.service import *
from views.client import *
from views.license import *
from views.ticket import *

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


