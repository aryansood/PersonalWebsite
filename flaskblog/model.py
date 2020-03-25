from flaskblog import db, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable =False)
	posts = db.relationship('Post', backref='user',lazy = True)

	def __repr__(self):
		return f"User('{self.name}','{self.password}')"
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(80), unique=True, nullable=False)
	description = db.Column(db.Text(), nullable = False)
	content = db.Column(db.Text(), nullable = False)
	imageurl = db.Column(db.Text(), nullable = False)
	post_time = db.Column(db.DateTime(), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


	def __repr__(self):
		return f"Post('{self.	title}','{self.subtitle}')"
class DateTime(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date_time = db.Column(db.DateTime(), nullable = False)


