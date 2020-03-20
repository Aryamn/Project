from lecyc import db , login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120) , unique = True , nullable = False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    # hall = db.Column(db.String(100), nullable=False)
    # roll_no = db.Column(db.String(10), unique=True, nullable=False)
    # mobile_no = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cycles = db.relationship('Cycle', backref='author', lazy=True)

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time_slot = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    features = db.Column(db.Text)
    reg_no = db.Column(db.String(20), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='cyc.png')
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    