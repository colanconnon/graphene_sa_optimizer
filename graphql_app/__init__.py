from flask import Flask
import graphene
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required


db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()

from .config import Config


def create_app(main=True, config_object=Config):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    from .auth.routes import auth_routes
    app.register_blueprint(auth_routes)
    from .schema import schema

    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )
    return app
