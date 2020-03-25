from flask import Flask ,render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, current_user
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dgsdgj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
db = SQLAlchemy(app)
db.init_app(app)
login_manager= LoginManager(app)
login_manager.login_view = 'user.login'
ckeditor = CKEditor(app)
user1 = current_user
class MyModelView(ModelView):
	edit_template = 'base_edit.html'
	def is_accessible(self):
		if not current_user.is_authenticated:
			return False
		else:
			if user1.id == 1:
				return True
			else:
				return False
admin = Admin(app)
from flaskblog.model import Post
admin.add_view(MyModelView(Post, db.session))
from flaskblog import user 
app.register_blueprint(user.bp)
from flaskblog import post
app.register_blueprint(post.bp)
