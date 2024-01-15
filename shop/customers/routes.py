from flask import redirect, render_template, url_for, flash, request,session
from shop import db, app, bcrypt, login_manager
from flask_login import login_required, current_user, logout_user, login_user

from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register



@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data,
                    username=form.username.data, 
                    email=form.email.data,
                    password=hash_password,
                    country=form.country.data,
                    state=form.state.data,
                    city=form.city.data,
                    address=form.address.data,
                    zipcode=form.zipcode.data
                    )
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customers/register.html',form=form)



@app.route('/customer/login', methods=['POST','GET'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['logged_in'] = True
            login_user(user)
            flash(f'You are login now','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customers/login.html',form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))

