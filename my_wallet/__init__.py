from flask import Flask

app = Flask(__name__)
#app.secret_key = ""
app.config.from_prefixed_env()




