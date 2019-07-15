
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from . import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('你已登录。')
        return redirect(url_for('manage_bp.news'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email', '').strip()).first()
        if user:
            if user.verify_password(password=request.form.get('password', '').strip()):
                login_user(user, True)
                return redirect(request.args.get('next') or url_for('manage_bp.news'))
            else:
                flash('密码错误。')
        else:
            flash('该用户不存在。')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('账号退出成功。')
    return redirect(url_for('main_bp.index'))
