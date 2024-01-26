from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123456@localhost/test'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://menu_mate_user:qOCOl4rmSffg05oDQwTdwbZNtZDDKBGQ@dpg-cmplptect0pc73f3i5lg-a.singapore-postgres.render.com/menu_mate'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return f'<Student {self.firstname}>'

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@app.route("/students", methods=["GET"])
def students_list():
    students = Student.query.all()
    return students_schema.dump(students)

@app.route("/students/create", methods=["POST"])
def student_create():
    firstname=request.json["firstname"]
    lastname=request.json["lastname"]
    new_student = Student(firstname, lastname)
    db.session.add(new_student)
    db.session.commit()
    return student_schema.jsonify(new_student)

@app.route("/students/<id>", methods=["GET"])
def student_detail(id):
    student = Student.query.get(id)
    return student_schema.dump(student)

@app.route("/students/update/<id>", methods=["PUT"])
def student_update(id):
    student = Student.query.get(id)
    firstname=request.json["firstname"]
    lastname=request.json["lastname"]
    student.firstname = firstname
    student.lastname = lastname
    db.session.commit()
    return student_schema.jsonify(student)

@app.route("/students/delete/<id>", methods=["DELETE"])
def student_delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return student_schema.jsonify(student)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)