from flask import Flask, Blueprint, render_template, request, jsonify
from functools import wraps
from flask_cors import CORS
from appleresolver import AppleResolver
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

CORS(app)

def get_cache(timeout=50):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if request.method == 'GET':
                return cache.cached(timeout=timeout)(f)(*args, **kwargs)
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/oauthservice')
def home():
    return 'Crezam OAuth Service'

@app.route('/oauthservice/apple', methods=['GET', 'POST'])
@get_cache(timeout=100)
def applelogin():
    if request.method == 'POST':
        apple_token = request.form['token']
        user = AppleResolver.authenticate(access_token=apple_token) or {}
        return jsonify(user)
    return render_template('apple.html')

@app.route('/oauthservice/google')
@get_cache(timeout=100)
def googlelogin():
    return render_template('google.html')


@app.route('/cameraservice')
def cameraservice():
    return render_template('camera.html')

# Runner Script
if __name__ == "__main__":
    # app.run(debug=True, port=3000) #Debugging
    app.run(host="0.0.0.0", port=3000)