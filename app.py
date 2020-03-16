from flask import Flask,render_template,url_for,flash,redirect
from form import RegistrationForm , LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '2912d4c2b6692117365c6cea'

@app.route("/")
@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('done')
        return redirect(url_for("register"))

    return render_template('form.html' , title = 'Register', form = form)


@app.route("/login",methods=['GET','POST'])
def login():
    form = RegistrationForm()
    return render_template('form.html' , title = 'login', form = form)


if __name__ == '__main__':
    app.run(debug=True)    