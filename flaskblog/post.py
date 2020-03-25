import functools
from flask_login import login_required,current_user, logout_user #check later if correct to add here.
from flask import(
	Blueprint, flash, g, redirect, render_template, 
	request, session, url_for
	)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskblog import db,login_manager
from flaskblog.model import Post, DateTime
from datetime import date
from sqlalchemy import extract
dict1 = { 1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
bp = Blueprint('blog', __name__, template_folder='template')
@bp.route('/')
def index():
	posts = Post.query.all()
	dates = DateTime.query.all() 
	return render_template('index.html', posts = posts, dates = dates)
@bp.route('/create', methods=['GET','POST'])
@login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form['description']
		content = request.form['content']
		imageurl = request.form['imageurl']
		post_time = date.today()
		l = DateTime.query.filter(extract('month', DateTime.date_time) == post_time.month).filter(extract('year', DateTime.date_time) == post_time.year).first()
		error = None
		if title is None:
			error = 'Required title'
		if error is None:
			post = Post(title = title, description = description, content = content, imageurl=imageurl, post_time=post_time,user= current_user)
			db.session.add(post)
			db.session.commit()
			if l == None:
				date1 = date(year=post_time.year,month=post_time.month,day=1)
				date2 = DateTime(date_time = date1)
				db.session.add(date2)
				db.session.commit()
			
			return redirect(url_for('user.register'))
	return render_template('create.html')
@bp.route('/posterview/<number>')
def posterview(number):
	post = Post.query.get(number)
	dates = DateTime.query.all() 
	return render_template('posterview.html', post = post, dates=dates)
@bp.route('/archive/<int:number>/<int:number1>')
def archive(number,number1):
	date2 = date(year = number, month = number1, day=dict1[number1])
	posts = Post.query.filter(extract('month', Post.post_time) == date2.month).filter(extract('year', Post.post_time) == date2.year).filter(extract('day', Post.post_time) <= date2.day).all()
	dates = DateTime.query.all()
	return render_template('archive.html', posts = posts, dates = dates )
@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('blog.index'))



