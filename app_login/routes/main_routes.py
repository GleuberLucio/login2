from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..user.user_controllers import get_all_users, get_user_by_email, get_user_by_id, create_user, save_user, update_user, delete_user, hash_password
from flask_login import login_required
from ..auth.auth_controllers import generate_token, send_password_reset_link

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/home', methods=['GET'])
def home():
    users = get_all_users()
    if not users:
        flash('No users found!', 'info')
        return render_template('home.html', users=[])
    return render_template('home.html', users=users)

@bp.route('/index', methods=['GET'])
def index():
    users = get_all_users()
    if not users:
        flash('No users found!', 'info')
        return render_template('index.html', users=[])
    return render_template('index.html', users=users)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('main.register'))
        
        if get_user_by_email(email):
            flash('Email already registered!', 'error')
            return redirect(url_for('main.register'))
        
        new_user = create_user(name=name, email=email, password=password)
        save_user(new_user) 
        flash('User registered successfully!', 'success')
        return redirect(url_for('main.home'))
    else:
        email = request.args.get('email')
        if email:
            existing_user = get_user_by_email(email)
            if existing_user:
                flash('Email already registered!', 'error')
                return redirect(url_for('main.register'))
    return render_template('register.html', email=email)

@bp.route('/delete/<int:user_id>', methods=['GET'])
@login_required
def delete(user_id):
    user = get_user_by_id(user_id)
    if not user:
        flash('User not found!', 'error')
    
    delete_user(user)
    flash('User deleted successfully!', 'success')
    return redirect(url_for('main.home'))

@bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
    user = get_user_by_id(user_id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('main.update', user_id=user_id))
        
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('main.home'))
        
        user.name = name
        user.email = email
        user.password_hash = hash_password(password)
        
        update_user(user)
        flash('User updated successfully!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('update.html', user=user)

@bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = get_user_by_email(email)
        
        
        if not user:
            flash('Email not registered!', 'error')
            return redirect(url_for('main.forgot'))
        
        token = generate_token(user.email)
        send_password_reset_link(user.email, token)
        
        flash('Password reset link sent to your email!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('forgot.html')
