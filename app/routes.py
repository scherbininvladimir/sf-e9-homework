from random import randint
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, login_manager, bcrypt
from .models import User, Event
from .forms import LoginForm, CreateUserForm, CreateEventForm


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route('/error')
def home():
    raise
    return None, 200

@app.route('/')
def list_events():
    if not current_user.is_authenticated:
        return redirect("/login")
    events = Event.query.all()
    return render_template('list_events.html', events=events)

@app.route('/edit_event/<int:id>', methods=["GET", "POST"])
@login_required
def edit_event(id):
    form = CreateEventForm()
    event = Event.query.filter_by(_id=id).first()
    if not event.author == current_user.login:
        error = "Вы можете редактировать только свои записи"
        return render_template('error.html', form=form, error=error)
    if request.method == 'POST':
        if form.validate_on_submit():
            event.start_time = request.form.get('start_time')
            event.end_time = request.form.get('end_time')
            event.title = request.form.get('title')
            event.description = request.form.get('description')
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=form,error = error)
    form.title.data = event.title
    form.start_time.data = event.start_time
    form.end_time.data = event.end_time
    form.description.data = event.description
    return render_template('edit_event.html', form=form)

@app.route('/delete_event/<int:id>')
@login_required
def delete_event(id):
    print(request.method)
    event = Event.query.filter_by(_id=id).first()
    if not event:
        error = "Неверный id"
        return render_template('error.html', error=error)
    if not event.author == current_user.login:
        error = "Вы можете удалять только свои записи"
        return render_template('error.html', error=error)
    db.session.delete(event)
    db.session.commit()
    return redirect('/')

@app.route("/create_event", methods=["GET", "POST"])
@login_required
def create_event():
    form = CreateEventForm()
    if request.method == "POST":
        if form.validate_on_submit():
            author = current_user.login
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            title = request.form.get('title')
            description = request.form.get('description')
            event = Event(author=author, start_time=start_time, end_time=end_time, title=title, description=description)
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        error = "Проверте корректность введенных данных"
        return render_template('error.html', form=form, error=error)
    return render_template('edit_event.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.login.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    current_user.authenticated=False
    db.session.add(current_user)
    db.session.commit()
    logout_user()
    return redirect('/')

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            login = request.form.get('login')
            if login in [u[0] for u in User.query.with_entities(User.login).all()]:
                error="Пользователь с таким именем уже зарегистрирован"
                return render_template('error.html',form=form,error = error)
            print(users) 
            password = request.form.get('password')
            user = User(login=login, password=bcrypt.generate_password_hash(password).decode('utf-8'))
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        error = "Провертьте правильность ввода"
        return render_template('error.html',form=form,error = error)
    return render_template("create_user.html", form=form)

