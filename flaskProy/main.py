from flask import Flask
from app.presentation.views import views
import os

app = Flask(__name__, static_folder=os.path.join('app', 'static'), template_folder=os.path.join('app', 'templates'))
app.register_blueprint(views)

if __name__ == "__main__":
    app.run(debug=True)
