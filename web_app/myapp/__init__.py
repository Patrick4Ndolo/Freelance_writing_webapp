import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from myapp.config import Config
from flask_mail import Mail
from flask_moment import Moment
import babel
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel, Locale
from flask_babel import lazy_gettext as _1
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/patrick/Freelance_writing_webapp/web_app/myapp/smartwriters.db'
app.config['SECRET_KEY'] = 'a78a98c724dff28bdc62234d'
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = "info"
login_manager.login_message = _1('Please login to access this page.')
mail = Mail(app)
moment = Moment(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)
csrf.init_app(app)


babel = Babel(app)

#checking if the application is not in debug mode.
#if not app.debug:
 #   if app.config['MAIL_SERVER']:
  #      auth = None
   #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
     #   secure = None
      #  if app.config['MAIL_USE_TLS']:
       #     secure = ()
     #   mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], 
      #      app.config['MAIL_PORT']), fromaddr='no_reply@' + app.config['MAIL_SERVER'], 
       #     toaddrs=app.config['ADMINS'], subject='Internal Failure', 
        #    credentials=auth, secure=secure)
       #ail_handler.setLevel(logging.ERROR)
        #app.logger.addHandler(mail_handler)

    #if not os.path.exists('log'):
     #   os.mkdir('logs')
    #file_handler = RotatingFileHandler('logs/Freelance_writing_webapp', maxBytes=10240, backupCount=10)
    #file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelnames)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    #file_handler.setLevel(logging.INFO)
    #app.logger.addHandler(file_handler)

    #app.logger.setLevel(logging.INFO)
    #app.logger.info('Myapp startup')


from myapp import routes, model, errors

