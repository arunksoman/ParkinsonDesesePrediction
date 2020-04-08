# init.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from .configurations import *
# from flask_login import current_user


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()
app = Flask(__name__)
Migrate(app, db.Model)

def create_app():
    app.config['SECRET_KEY'] = '9OLWxNDhfvhjvj4o83j4K4iu3545860nhgkopO'
    app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

    # For XAMPP
    # app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    app.config['QLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/db_parkinson'

    # For freemysqlhosting.net 
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql12311054:j6vcg7VTx7@sql12.freemysqlhosting.net/sql12311054'

    # For AMPPS
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@127.0.0.1/db_project'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'guest.login'
    login_manager.init_app(app)

    from .Models.models import Users
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Users.query.get(int(user_id))

    # blueprint for guest routes in our app
    from .Guest import guest as guest_blueprint
    app.register_blueprint(guest_blueprint.guest)

    # blueprint for admin routes in our app
    from .Admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint.adminNew_blueprint)
    from .Admin.admin import admin
    admin.init_app(app)
    mail.init_app(app)

    # blueprint for user routes in our app
    from .User import user as user_blueprint
    app.register_blueprint(user_blueprint.user)

    # blueprint for user routes in our app
    from .Doctor import doctor as doctor_blueprint
    app.register_blueprint(doctor_blueprint.doctor)

    # blueprint for non-auth parts of app
    from Project.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()