from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.db import get_db
from app.models import User

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        cursor = db.cursor(dictionary=True)
        # We use simple raw SQL query (parameterized to prevent SQL injection)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()
        print(user_data)
        cursor.close()
        db.close()

        if user_data:
            user = User(str(user_data['id']), user_data['username'])
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('lessons.index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('lessons.index'))
