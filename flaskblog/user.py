import functools
from flask import(
	Blueprint, flash, g, redirect, render_template, 
	request, session, url_for
	)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskblog import db
from flaskblog.model import User
from flask_login import login_user
bp = Blueprint('user', __name__, template_folder='template')

@bp.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['name']
		password = request.form['password']
		secret_pass = request.form['secret']
		user = User.query.filter_by(name = username).first()
		error = None
		if not username:
			error = 'username is required'
		if not password:
			error = 'password is required'
		if secret_pass != '':
			error = 'Secret code is wrong'

		if user:
			error = 'User is registered try a different name'
		if error is None:
			admin = User(name=username, password=generate_password_hash(password))
			db.session.add(admin)
			db.session.commit()
			flash('your account created')
			return redirect(url_for('user.register'))
		flash(error)
		    
	return render_template('register.html')
@bp.route('/login', methods= ['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['name']
		password = request.form['password']
		admin = User.query.filter_by(name = username).first()
		if admin:
			result = check_password_hash(admin.password,password)
			if result:
				login_user(admin, remember=True)
				flash('login succes')
				return redirect(url_for('blog.index'))
			else:
				flash('password is wrong')
		else:
			flash('user is not registered')
	return render_template('login.html')


