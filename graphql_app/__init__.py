from flask import Flask
import graphene
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

from .config import Config


def create_app(main=True, config_object=Config):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    from .schema import schema

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
    )
    return app
