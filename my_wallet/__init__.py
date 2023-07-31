from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)


load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config.from_prefixed_env()

app.config['PERMANENT_SESSION_LIFETIME'] = 15




