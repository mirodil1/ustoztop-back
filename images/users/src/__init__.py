from celery import Celery, Task

from flask import Flask
from flask_jwt_extended import JWTManager


def celery_init(app: Flask) -> Celery:
    print("INIt")
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            print("Task is being       called")  # Add this lin
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)

    JWTManager(app)

    from src.db import db
    db.init_app(app)

    from src import models
    with app.app_context():
        db.drop_all()
        db.create_all()
        # default roles initialization
        if not models.Role.query.filter_by(role_name="admin").first():
            admin_role = models.Role(role_name="admin")
            db.session.add(admin_role)
        if not models.Role.query.filter_by(role_name="turor").first():
            adult_role = models.Role(role_name="tutor")
            db.session.add(adult_role)
        if not models.Role.query.filter_by(role_name="learning_center").first():
            child_role = models.Role(role_name="learning_center")
            db.session.add(child_role)
        if not models.Role.query.filter_by(role_name="student").first():
            child_role = models.Role(role_name="student")
            db.session.add(child_role)
        db.session.commit()

    from src.routes.v1 import router as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')
    
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis:6379/0",
            result_backend="redis://redis:6379/0",
            task_ignore_result=True,
            include=["src.tasks"]
        ),
    )
    app.config.from_prefixed_env()
    celery_init(app)
     
    return app
