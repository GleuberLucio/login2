from app_login import login_manager
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app_login.controllers import get_user_by_email, verify_password
from flask_login import login_user
from app_login.controllers import get_user_by_id


login_manager.login_view = 'auth.login'  # Set the login view for Flask-Login
login_manager.login_message = 'Por favor realize o log in para acessar esta página.'  # Custom login message
login_manager.login_message_category = 'info'  # Custom category for the login message

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)  
    return user

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = get_user_by_email(email)
        if not user or not verify_password(user.password_hash, password):
            flash('Invalid email or password!', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)  
        flash('Logged in successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    from flask_login import logout_user
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))