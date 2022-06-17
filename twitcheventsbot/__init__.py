import secrets
from flask import Flask

app = Flask(__name__)
app.secret_key = secrets.token_hex()
