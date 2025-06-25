from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/apptarefas.sqlite'
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from .models import User
    from .routes import main
    from .auth import auth
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    with app.app_context():
        db.create_all()
        
    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))