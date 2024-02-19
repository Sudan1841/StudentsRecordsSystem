'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Student:
Description: Homework 03 - Routes for the SQLAlchemy Relationship Web App
'''


from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db


from app.models import User, St  # Adjust the import as per your models
from .forms import AddStudentForm, SignUpForm, LoginForm  # Adjust the import as per your forms






@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(form.passwd.data)
        new_user = User(id=form.id.data, name=form.name.data, about=form.about.data, passwd_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and check_password_hash(user.passwd_hash, form.passwd.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('recipes'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/student_info', methods=['GET', 'POST'])
@login_required
def student_info():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = St(
            name=form.name.data, 
            age=form.age.data,
            grade=form.grade.data)
        db.session.add(new_student)
        db.session.commit()
        flash('New student added successfully!', 'success')
        return redirect(url_for('student_info'))

    students = St.query.all()
    return render_template('student_info.html', form=form, students=students)





@app.route('/add_student/create', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = St(
            name=form.name.data, 
            age=form.age.data,
            grade=form.grade.data)
        db.session.add(new_student)
        db.session.commit()
        flash('New student added successfully!', 'success')
        return redirect(url_for('student_info'))
    return render_template('add_student.html', form=form)



@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = St.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('student_info'))

