from flask import render_template, flash, url_for , request
from werkzeug.utils import redirect
from app import app , db
from app.forms import LoginForm , RegistrationForm
from flask_login import current_user, login_user, login_required , logout_user
from app.models import User, Course
from werkzeug.urls import url_parse

@app.route('/home')  # bayad bere to home page(site landing page)
def home():
    courses = Course.query.all()
    return render_template('home.html', title='Home' , courses = courses)

@app.route('/landing_page')
def landing_page():
    courses = Course.query.all()
    return render_template('landing_page/index.html', title='Landing Page' , courses = courses)

@app.route('/about_us')
def about_us():
    return render_template('landing_page/about_us.html', title='About_us' )


@app.route('/index')  # manzoor az index va home hamon dashboard ast ... :)
@login_required
def index():
    return render_template('index.html', title='Index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/allCourses' , methods=['GET', 'POST'])
@login_required
def allCourses():
    courses = Course.query.all()
    if request.method == 'POST':
        filter = request.form['course_name_filter']
        if filter is not '':
            filtered_courses = Course.query.filter_by(name=filter)
            courses = filtered_courses
    return render_template('allCourses.html', title='all courses' , courses = courses)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404