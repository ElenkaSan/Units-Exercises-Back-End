from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS GO BELOW!

class Pet(db.Model):
    __tablename__ = "pets"
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    name = db.Column(db.Text, 
                   nullable=False)
    species = db.Column(db.Text, 
                   nullable=False)
    photo_url = db.Column(db.Text)
                
    age = db.Column(db.Integer) 
                  
    notes = db.Column(db.Text) 
               
    available = db.Column(db.Text,
                    nullable = False, 
                    default = True)
    @property
    def pet_name(self):
       return f"{self.name}"

#     def __repr__(self):
#         return f"<Department {self.dept_code} {self.dept_name} {self.phone} >"

# def get_directory():
#     all_emps = Employee.query.all()

#     for emp in all_emps:
#         if emp.dept is not None:
#             print(emp.name, emp.dept.dept_name, emp.dept.phone)
#         else:
#             print(emp.name)


# def get_directory_join():
#     directory = db.session.query(
#         Employee.name, Department.dept_name, Department.phone).join(Department).all()

#     for name, dept, phone in directory:
#         print(name, dept, phone)


# def get_directory_join_class():
#     directory = db.session.query(Employee, Department).join(Department).all()

#     for emp, dept in directory:
#         print(emp.name, dept.dept_name, dept.phone)


# def get_directory_all_join():
#     directory = db.session.query(
#         Employee.name, Department.dept_name, Department.phone).outerjoin(Department).all()

#     for name, dept, phone in directory:
#         print(name, dept, phone)
