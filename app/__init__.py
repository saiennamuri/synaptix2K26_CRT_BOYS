from flask import Flask
from .config import Config
from .extensions import db
from .routes import all_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app