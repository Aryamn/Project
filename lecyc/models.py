from lecyc import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    name = db.Column(db.String(100),nullable=False)
    hall = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(10), unique=True, nullable=False)
    mobile_no = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cycles = db.relationship('Cycle', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    date_avail = db.Column(db.Integer,nullable=False,default=1)
    month_avail = db.Column(db.Integer,nullable=False,default=1)

    time_slot_start = db.Column(db.Integer, nullable=False,
                          default=1)

    time_slot_end = db.Column(db.Integer, nullable=False,
                          default=2)

    time_slot_meri_start = db.Column(db.String(4),nullable=False,default='am')
    time_slot_meri_end = db.Column(db.String(4),nullable=False,default='am')

    features = db.Column(db.Text)
    reg_no = db.Column(db.String(20), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratings = db.Column(db.Integer , default = 0)
    sell = db.Column(db.Boolean , default=False)
    lend = db.Column(db.Boolean , default=False)
    status = db.Column(db.Boolean , default=True)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

class Comments(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posting_id = db.Column(db.Integer)