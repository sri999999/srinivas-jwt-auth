"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("config.Config")

try:
    from src import models
    from src.routes import api_router

    app.register_blueprint(api_router)

    with app.app_context():
        models.db.create_all()
        models.db.session.commit()
except Exception as e:
    import traceback

    traceback.print_exc()
    app.logger.error(e)
