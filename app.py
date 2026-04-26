from flask import Flask,render_template,redirect,url_for,jsonify,request,flash
from models import db, Student
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Prefer env so Linux/server hosts differ from Windows; Heroku uses postgres://
_default_db = 'postgresql://postgres:123456@localhost:5432/student_registration'
_database_url = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI') or _default_db
if _database_url.startswith('postgres://'):
    _database_url = _database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = _database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database created!")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey123')
# Absolute path so uploads work when cwd is not the project dir (e.g. PythonAnywhere WSGI)
_app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(_app_dir, 'static', 'uploads')

@app.route('/')

def home():
    students = Student.query.all()
    return render_template('home.html', students=students)

@app.route('/register',methods = ['GET','POST'])
def register():
    try:
        if request.method == 'POST':
            name  = request.form['name']
            email = request.form['email']
            roll_number = request.form['roll_number']
            semester = request.form['semester']
            batch = request.form['batch']
            mobile_number = request.form['mobile_number']
            photo = request.files['photo']
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db_photo = filename
            else:
                db_photo = None

            new_student = Student(name=name, email=email, roll_number=roll_number, semester=semester, batch=batch, mobile_number=mobile_number, photo=db_photo)
            db.session.add(new_student)
            db.session.commit()
            flash("Student registered successfully!")
            return redirect(url_for('home'))
        return render_template('register.html')
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('register'))

@app.route('/edit/<int:id>',methods = ['GET','POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.roll_number = request.form['roll_number']
        student.semester = request.form['semester']
        student.batch = request.form['batch']
        student.mobile_number = request.form['mobile_number']
        photo = request.files['photo']
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            student.photo = filename
        db.session.commit()
        flash("Student details updated successfully!")
        return redirect(url_for('home'))
    return render_template('edit.html', student=student)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    print(student)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)