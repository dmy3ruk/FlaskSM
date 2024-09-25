import datetime
from flaskSM import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), default='default.jpg', nullable=False)
    password = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(255), nullable=True)

    posts = db.relationship('Post', back_populates='user')
    def __repr__(self):
        return f'User(" {self.username}", "{self.email}", "{self.image_file} )'


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    file = db.Column(db.Text(100), nullable=True)

    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', backref='post', lazy=True)  # Зв'язок з коментарями
    likes = db.relationship('Like', backref='post', lazy=True)  # Зв'язок з лайками

    def __repr__(self):
        return f'User("{self.title}", "{self.date_posted}", "{self.user.username}" )'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Текст коментаря
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)  # Дата коментаря
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)  # Зв'язок з постом
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Зв'язок з користувачем

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_liked = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)  # Дата лайка
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)  # Зв'язок з постом
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Зв'язок з користувачем

    def __repr__(self):
        return f"Like('Post ID: {self.post_id}', 'User ID: {self.user_id}')"
