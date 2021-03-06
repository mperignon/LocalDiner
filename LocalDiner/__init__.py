from flask import Flask
app = Flask(__name__,
            template_folder="templates",
            instance_relative_config=True)

app.config.from_pyfile('config.py')

from LocalDiner import views