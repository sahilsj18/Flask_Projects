from flask import Flask
from routes import blog_blueprint
app = Flask(__name__)

# Register the routes from routes.py
app.register_blueprint(blog_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
