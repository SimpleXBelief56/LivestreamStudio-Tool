from flask import Flask
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

app = Flask(__name__)

from livestreamstudio import routes