from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import logging.handlers


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

handler = logging.handlers.RotatingFileHandler('test_app_log.txt', maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)


from test_app import routes, models, forms, models, helpers, pay_methods



