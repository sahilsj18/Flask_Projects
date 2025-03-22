from flask import Flask
from routes import app as routes_blueprint  # Import Blueprint

app = Flask(__name__)

# Register the Blueprint properly
app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
