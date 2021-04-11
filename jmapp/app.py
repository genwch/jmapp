from flask import Flask, redirect
from flask_jwt_extended import JWTManager
from . import routes as rt

from . import lib as lib

app = Flask(__name__)
secret = "jobmatch-secret"
app.config['JWT_SECRET_KEY'] = secret
app.secret_key = secret
jwt = JWTManager(app)

for o in rt.__route__:
    app.register_blueprint(o.get("route"), url_prefix=o.get("prefix", "/"))

# app.register_blueprint(rt.home, url_prefix="/")
# app.register_blueprint(rt.login, url_prefix="/")
# app.register_blueprint(rt.job, url_prefix="/job")
# app.register_blueprint(rt.profile, url_prefix="/profile")


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return redirect("/login?msg=Token Expired")
