from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
import os
from dotenv import load_dotenv
from models import db, Homework, SchoolClass, Subject, init_defaults

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db.init_app(app)

ADMIN_PASSWORD = 'sysyc'

def login_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('admin'))
        else:
            flash('Неверный пароль', 'error')
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/homework')
def homework_page():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    homework = Homework.query.order_by(Homework.deadline).all()
    return render_template('homework.html', homework=homework)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
@login_required
def admin():
    homework = Homework.query.order_by(Homework.deadline).all()
    classes = SchoolClass.query.order_by(SchoolClass.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin.html', 
                         homework=homework,
                         classes=classes,
                         subjects=subjects,
                         datetime=datetime)

@app.route('/add_homework', methods=['POST'])
@login_required
def add_homework():
    if request.method == 'POST':
        class_id = request.form.get('class')  
        subject_id = request.form.get('subject')  
        task = request.form.get('task')
        deadline = datetime.strptime(request.form.get('deadline'), '%Y-%m-%d')
        
        homework = Homework(
            class_id=class_id,
            subject_id=subject_id,
            task=task,
            deadline=deadline
        )
        db.session.add(homework)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_homework/<int:id>', methods=['POST'])
@login_required
def delete_homework(id):
    homework = Homework.query.get_or_404(id)
    db.session.delete(homework)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_class', methods=['POST'])
@login_required
def add_class():
    if request.method == 'POST':
        name = request.form.get('class_name')  
        school_class = SchoolClass(name=name)
        db.session.add(school_class)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_class/<int:id>', methods=['POST'])
@login_required
def delete_class(id):
    school_class = SchoolClass.query.get_or_404(id)
    db.session.delete(school_class)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_subject', methods=['POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('subject_name')  
        subject = Subject(name=name, is_custom=True)
        db.session.add(subject)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_subject/<int:id>', methods=['POST'])
@login_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.is_custom:  
        db.session.delete(subject)
        db.session.commit()
    return redirect(url_for('admin'))

with app.app_context():
    db.create_all()
    init_defaults()

if __name__ == '__main__':
    app.run(debug=True)
