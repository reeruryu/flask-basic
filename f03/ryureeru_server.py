
from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from view import login
from control.user_mgmt import User
import os

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'ryureeru_key' # app.secret_key =os.urandom(24)

app.register_blueprint(login.login_test, url_prefix='/ryureeru')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(number):
    return User.get(number)


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

@app.route("/index")
def index():
    if current_user.is_authenticated:
        #print(current_user.user_id)
        return render_template("index.html", user_id=current_user.user_id)
    else:
        return render_template("index.html")

@app.route("/mypage")
@login_required
def mypage():
    if current_user.is_authenticated:
        #print(current_user.user_id)
        return render_template("mypage.html", user_id=current_user.user_id)

@app.route("/test")
@login_required
def test():
    if current_user.is_authenticated:
        #print(current_user.user_id)
        return render_template("test.html", user_id=current_user.user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
