from flask import Flask
from db_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session, SqlAlchemySessionInterface
from flask_login import LoginManager


#Instância e configura a aplicação app do Flask
app = Flask(__name__)
app.config.from_object(Config)

#Instância do ORM e a Sessão do Usuário
db = SQLAlchemy(app)
sess = Session(app)
app.session_interface = SqlAlchemySessionInterface(app, db, "session", "sess_")

#Configuração das Migrações
#migrate = Migrate(app, db)

#Instância e configuração do gerenciador de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'adm_index'