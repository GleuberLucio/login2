from app_login import login_manager
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app_login.controllers import get_user_by_email, verify_password
from flask_login import login_user
from app_login.controllers import get_user_by_id, save_user
from app_login.auth_controllers import verify_token, hash_password


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

@auth_bp.route('/reset-pass/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_token(token)
    
    if not email:
        flash('Invalid or expired token!', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.reset_pass', token=token))
        if not new_password:
            flash('Password cannot be empty!', 'error')
            return redirect(url_for('auth.reset_pass', token=token))
        
        user = get_user_by_email(email)
        user.password_hash = hash_password(new_password)
        save_user(user)
        return redirect(url_for('auth.login'))
    return render_template('reset_pass.html', token=token, email=email)