from lecyc.models import User,Cycle
from lecyc.form import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect
from lecyc import app

@app.route("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('done')
        return redirect(url_for("register"))

    return render_template('form.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    return render_template('form.html', title='login', form=form)
