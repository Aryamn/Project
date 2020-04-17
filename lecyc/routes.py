import random
import os
import stripe
from PIL import Image
from lecyc.models import User, Cycle
from lecyc.form import (RegistrationForm, LoginForm, UpdateAccount,
                        PostForm, RequestResetForm, ResetPasswordForm, Ratings)
from flask import abort, render_template, url_for, flash, redirect, request
from lecyc import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")  # Cycles.order_by(Post.ratings.desc())
def home():
    page = request.args.get('page', 1, type=int)
    posts = Cycle.query.order_by(Cycle.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/home/start_time")  # Cycles.order_by(Post.ratings.desc())
def hometime():
    page = request.args.get('page', 1, type=int)
    posts = Cycle.query.order_by(Cycle.date_avail.desc()).order_by(Cycle.time_slot_start.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/home/ratings")  # Cycles.order_by(Post.ratings.desc())
def homerate():
    page = request.args.get('page', 1, type=int)
    posts = Cycle.query.order_by(Cycle.ratings.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password,name=form.name.data,hall=form.hall.data,
                    roll_no=form.roll_no.data,mobile_no=form.mobile_no.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login','success')
        print('done')
        return redirect(url_for("login"))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login Unsuccesfull. Please check your email and password','danger')
           

    return render_template('login.html', title='login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = str(random.randint(0, 123456789123456789))
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pic', picture_fn)

    output_size = (125, 125)
    f = Image.open(form_picture)
    f.thumbnail(output_size)

    f.save(picture_path)

    return picture_fn


def save_picture_post(form_picture):
    random_hex = str(random.randint(0, 123456789123456789))
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pic', picture_fn)

    output_size = (250, 250)
    f = Image.open(form_picture)
    f.thumbnail(output_size)

    f.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.roll_no = form.roll_no.data
        current_user.mobile_no = form.mobile_no.data
        current_user.hall = form.hall.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.hall.data = current_user.hall
        form.roll_no.data = current_user.roll_no
        form.mobile_no.data = current_user.mobile_no

    image_file = url_for(
        'static', filename='profile_pic/'+current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    picture_file = ""
    if form.validate_on_submit():
        if form.sell.data != form.lend.data:
            if form.image.data:
                picture_file = save_picture_post(form.image.data)
                post = Cycle(title=form.title.data, time_slot_start=form.time_slot_start.data,
                            time_slot_end=form.time_slot_end.data, time_slot_meri_start=form.time_slot_meri_start.data,
                            time_slot_meri_end = form.time_slot_meri_end.data,
                            month_avail=form.month_avail.data , date_avail=form.date_avail.data,
                            features=form.features.data, reg_no=form.reg_no.data,
                            price=form.price.data, author=current_user, sell=form.sell.data, lend=form.lend.data, image_file=picture_file)
            else:
                post = Cycle(title=form.title.data, time_slot_start=form.time_slot_start.data,
                            time_slot_end=form.time_slot_end.data, time_slot_meri_start = form.time_slot_meri_start.data,
                            time_slot_meri_end = form.time_slot_meri_end.data,
                            month_avail=form.month_avail.data , date_avail=form.date_avail.data,
                            features=form.features.data, reg_no=form.reg_no.data,
                            price=form.price.data, author=current_user, sell=form.sell.data, lend=form.lend.data)
           
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
    return render_template("create_post.html", title="New Post", form=form)


# @app.route("/post/<post_id>")
# def post(post_id):
#     post = Cycle.query.get_or_404(post_id)
#     return render_template("post.html", title=post.title, post=post)


@app.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Cycle.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture_post(form.image.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.features = form.features.data
        post.price = form.price.data

        post.time_slot_start = form.time_slot_start.data
        post.time_slot_end = form.time_slot_end.data
        post.time_slot_meri = form.time_slot_meri.data
        post.month_avail = form.month_avail.data
        post.date_avail = form.date_avail.data

        post.reg_no = form.reg_no.data
        post.sell = form.sell.data
        post.lend = form.lend.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post',post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.features.data = post.features

        form.time_slot_start.data = post.time_slot_start
        form.time_slot_end.data = post.time_slot_end
        form.time_slot_meri.data = post.time_slot_meri
        form.date_avail.data = post.date_avail
        form.month_avail.data = post.month_avail
        

        form.reg_no.data = post.reg_no
        form.price.data = post.price
        form.sell.data = post.sell
        form.lend.data = post.lend
        form.image.data = post.image_file

    image_file = url_for('static', filename='post_pic/'+post.image_file)
    return render_template("create_post.html", title="New Post", form=form, image_file=image_file)

@app.route("/post/<post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Cycle.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='noreply@demo.com',
                    recipients=[user.email])

    msg.body = "To reset your password , visit the following link:" + url_for('reset_token' , token=token , _external=True)
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    
    if user==None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        print('done')
        return redirect(url_for("login"))
    return render_template('reset_token.html',title='Reset Password', form=form)

@app.route("/post/<post_id>",methods = [ 'GET', 'POST' ])
@login_required
def post(post_id):
    post = Cycle.query.get_or_404(post_id)
    form = Ratings()

    if form.validate_on_submit():
        if form.rating.data:
            post.ratings += (form.rating.data/5)
            db.session.commit()
            return redirect(url_for("post",post_id=post.id))

    return render_template("post.html", title=post.title, post=post,form=form)    


@app.route("/user/<string:username>")  # Cycles.order_by(Post.ratings.desc())
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Cycle.query.filter_by(author=user).order_by(Cycle.date_avail.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts , user=user)


stripe_keys = {
  'secret_key': 'sk_test_yga6FQ5RcHpHwn93UFEN1E3i004K23V7XU',
  'publishable_key': 'pk_test_H7xCQ8458Q2adRXHB17C24jU00b9y1Yi7T'
}

stripe.api_key = stripe_keys['secret_key']


@app.route("/post/<post_id>/payment",methods=['POST','GET'])
@login_required
def payment(post_id):
    post = Cycle.query.get_or_404(post_id)
    return render_template('payment.html',key=stripe_keys['publishable_key'],post=post)

@app.route("/post/<post_id>/charge", methods=['POST'])
def charge(post_id):
    post = Cycle.query.get_or_404(post_id)

    amount = post.price*100

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='INR',
        description=post.title
    )

    post.status=False
    db.session.commit()

    return render_template('charge.html', amount=amount)

@app.route("/post/<post_id>/confirm",methods=['POST','GET'])
@login_required
def confirm(post_id):
    post = Cycle.query.get_or_404(post_id)
    post.status=True
    db.session.commit()

    return redirect(url_for('home'))

    

