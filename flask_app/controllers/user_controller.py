from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register_user():
    print(request.form)

    if not User.validate_new_user(request.form):
        return redirect('/')

    new_user = {
        **request.form,
        # 'password': bcrypt.generate_password_hash(request.form['password'])
    }
    new_user_id = User.save(new_user)
    session['uid'] = new_user_id
    return redirect('/')

@app.route('/login', methods=['POST'])
def login_user():

    found_user = User.validate_login(request.form)

    if not found_user:
        return redirect('/')
    
    session['uid'] = found_user.id

    return redirect('/dashboard')
    

@app.route('/dashboard')
def dashboard():

    if not 'uid' in session:
        flash("ACCESS DENIED","login")
        return redirect('/')
    logged_in_user = User.get_user_id(session['uid'])

    return render_template('dashboard.html', user = logged_in_user)

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out","logout")
    return redirect('/')