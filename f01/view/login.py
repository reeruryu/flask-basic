from flask import Flask, Blueprint, request, render_template, flash, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user
from control.user_mgmt import User
import datetime

login_test = Blueprint('login', __name__)


@login_test.route('/set_id', methods=['GET', 'POST'])
def set_id():
    if request.method == 'GET':
        # print('set_id', request.headers)
        #print('set_id', request.args.get('user_id'))
        return redirect(url_for('login.test_login'))
    else:
        # print('set_id', request.headers)
        # content type 이 application/json 인 경우
        # print('set_id', request.get_json())
        print('set_id', request.form['user_id'], request.form['user_pw'])
        if User.find(request.form['user_id'], request.form['user_pw'])==None:
            flash('아이디 비번이 틀렸습니다')
            return render_template("index.html")
        else:
            user = User.create(request.form['user_id'], request.form['user_pw'])
            # https://docs.python.org/3/library/datetime.html#timedelta-objects
            login_user(user, remember=True, duration=datetime.timedelta(days=365))
            print(current_user.user_id)
            return redirect(url_for('login.test_login'))

    # return redirect('/ryureeru/test_login')
    # return make_response(jsonify(success=True), 200)


@login_test.route('/logout')
def logout():
    #User.delete(current_user.id) 탈퇴
    logout_user()
    return redirect(url_for('login.test_login'))


@login_test.route('/test_login')
def test_login():
    if current_user.is_authenticated:
        print(current_user.user_id)
        return render_template('index.html', user_id=current_user.user_id)
    else:
        print("x")
        return render_template('index.html')
