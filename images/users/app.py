from flask import Flask
from flask_jwt_extended import JWTManager
    

def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)
    JWTManager(app)
    from src.db import db
    db.init_app(app)
    import src.models
    with app.app_context():
        db.create_all()

    from src.routes.v1 import router as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')
    print(app.url_map)
    return app

