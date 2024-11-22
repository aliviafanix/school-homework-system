from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False, unique=True)
    homeworks = db.relationship('Homework', backref='school_class', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    is_custom = db.Column(db.Boolean, default=False)
    homeworks = db.relationship('Homework', backref='subject_rel', lazy=True)

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    task = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'class': self.school_class.name,
            'subject': self.subject_rel.name,
            'task': self.task,
            'deadline': self.deadline.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

DEFAULT_CLASSES = [
    "5В"
]

DEFAULT_SUBJECTS = [
    "Русский язык",
    "Родной язык",
    "Математика",
    "Литература",
    "Родная литература",
    "Английский язык",
    "Немецкий язык",
    "История",
    "Обществознание",
    "Физика",
    "Химия",
    "Биология",
    "География",
    "ИЗО",
    "ОБЖ",
    "Музыка",
    "Технология",
    "Физкультура"
]

def init_defaults():
    # Добавляем классы по умолчанию
    for class_name in DEFAULT_CLASSES:
        if not SchoolClass.query.filter_by(name=class_name).first():
            db.session.add(SchoolClass(name=class_name))
    
    # Добавляем предметы по умолчанию
    for subject_name in DEFAULT_SUBJECTS:
        if not Subject.query.filter_by(name=subject_name).first():
            db.session.add(Subject(name=subject_name, is_custom=False))
    
    db.session.commit()
