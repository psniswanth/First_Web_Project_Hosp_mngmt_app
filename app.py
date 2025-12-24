from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import time
import random


app = Flask(__name__)

app.config['SECRET_KEY'] = '123453'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable = False, unique= True)
    email = db.Column(db.String(150),nullable = False, unique= True)
    password = db.Column(db.String(150),nullable = False)
    role = db.Column(db.String(50),nullable = False)
    blacklisted = db.Column(db.Boolean,default=False)

    spl_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable=True)

    department = db.relationship('Department', backref='doctors')


class Department(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),nullable = False, unique= True)
    info = db.Column(db.String(300),nullable = False)


class Appointments(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    app_date = db.Column(db.Date, nullable=False) 
    app_time = db.Column(db.Time,nullable=False) 
    app_status = db.Column(db.String(30),nullable=False, default="Assigned")

    patient_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) 
    doctor_id = db.Column(db.Integer,db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) 
    
    patient = db.relationship('User',foreign_keys='Appointments.patient_id',backref=db.backref('patient_appointments', passive_deletes=True))

    doctor = db.relationship('User',foreign_keys='Appointments.doctor_id',backref=db.backref('doctor_appointments', passive_deletes=True))


    visit_type = db.Column(db.String(50), nullable=True)
    tests_done = db.Column(db.String(50), nullable=True) 
    diagnosis = db.Column(db.String(50),  nullable=True) 
    prescription = db.Column(db.String(50), nullable=True) 
    medicine= db.Column(db.String(50), nullable=True)

class DoctorAvailability(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    doctor_id = db.Column(db.Integer,db.ForeignKey('user.id', ondelete="CASCADE"),nullable=False)
    date = db.Column(db.Date, nullable=False)

    morning_slot = db.Column(db.Boolean, default=False)
    evening_slot = db.Column(db.Boolean, default=False)

    doctor = db.relationship('User',backref=db.backref('availability', cascade="all, delete-orphan", passive_deletes=True))

def initialize_database():
    admin = User.query.filter_by(role='admin').first()
    if (not admin):
        new_admin = User(username='admin',email='hospital@gmail.com',password='admin123',role='admin')
        db.session.add(new_admin)
        db.session.commit()
        print("No prexisting admin was found , created new admin.")


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        name = request.form['username']
        mail = request.form['email']
        pwd = request.form['password']

        existing_user = User.query.filter_by(username=name,email=mail).first()
        if existing_user:
            return redirect(url_for('login'))
        
        new_user = User(username=name,email=mail,password=pwd,role="patient")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        name = request.form['username']
        pwd = request.form['password']

        existing_user = User.query.filter_by(username=name,password=pwd).first()

        if existing_user:
            session['id'] = existing_user.id
            session['username'] = existing_user.username
            session['role'] = existing_user.role

            if existing_user.role=="patient":
                return redirect(url_for('patient_dashboard'))
            elif existing_user.role=="admin":
                return redirect(url_for('admin_dashboard'))
            elif existing_user.role=="doctor":
                return redirect(url_for('doctor_dashboard'))
        else:
            return render_template('login.html')
        
    return render_template('login.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    if session.get('role')=="patient":
        departments = Department.query.all()
        appointments = Appointments.query.filter_by(patient_id=session['id'],app_status="Assigned").all()

        return render_template('patient_dashboard.html',departments=departments,appointments=appointments)
    else:
        return redirect(url_for('login'))

@app.route('/patient_dashboard/department/<int:spl_id>')
def department_view(spl_id):
    dept = Department.query.filter_by(id=spl_id).first()
    doctors = User.query.filter_by(spl_id=spl_id,role="doctor").all()

    return render_template('department.html',dept=dept,doctors=doctors)

@app.route('/admin_dashboard',methods=["GET","POST"])
def admin_dashboard():
    if session.get('role')=="admin":
        if request.method=="GET":

            doctors = User.query.filter_by(role='doctor').all()
            patients = User.query.filter_by(role='patient').all()
            appointments = Appointments.query.all()
                
            return render_template('admin_dashboard.html',doctors=doctors,patients=patients,appointments=appointments)
        
        else:
            query = request.form['search']

            doctors = User.query.filter_by(role='doctor').all()
            patients = User.query.filter_by(role='patient').all()
            appointments = Appointments.query.all()

            if query:
                doctors = User.query.filter(User.role == "doctor",(User.username.ilike(f"%{query}%")) | (User.id == query)).all()

                patients = User.query.filter(User.role == "patient",(User.username.ilike(f"%{query}%")) | (User.id == query)).all()
                appointments = Appointments.query.all()
            
            return render_template('admin_dashboard.html',doctors=doctors,patients=patients,appointments=appointments)

    else:
        return redirect(url_for('login'))

    
@app.route('/admin_dashboard/create_doctor',methods=["GET","POST"])
def create_doctor():
    if request.method=="POST":
        name = request.form['username']
        mail = request.form['email']
        pwd = request.form['password']
        spl_id = request.form['spl_id']

        new_doc = User(username=name,email=mail,password=pwd,spl_id=spl_id,role="doctor")
        db.session.add(new_doc)
        db.session.commit()

        return redirect(url_for('admin_dashboard'))
        
    else:
        return render_template('create_doctor.html')

@app.route('/admin_dashboard/delete_doctor/<int:id>')
def delete_doctor(id):
    doctor = User.query.filter_by(id=id).first()
    Appointments.query.filter_by(doctor_id=id).delete()

    db.session.delete(doctor)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/delete_patient/<int:id>')
def delete_patient(id):
    patient = User.query.filter_by(id=id).first()
    Appointments.query.filter_by(patient_id=id).delete()

    db.session.delete(patient)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if session.get('role')=="doctor":
        name = session.get('username')
        id = session.get('id')
        appointments = Appointments.query.filter_by(doctor_id=id,app_status="Assigned")
        patient_list = Appointments.query.filter_by(doctor_id=id)
        
        return render_template('doctor_dashboard.html',appointments=appointments,assigned_appointments=patient_list)
    else:
        return redirect(url_for('login'))
    


@app.route('/doctor_dashboard/update/<int:id>',methods=["GET","POST"])
def update_history(id):
    app = Appointments.query.filter_by(id=id).first()

    if request.method=="POST":
        visit_type = request.form['visit_type']
        test_done = request.form['test_done']
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']


        app.visit_type = visit_type
        app.tests_done = test_done
        app.diagnosis = diagnosis
        app.prescription = prescription

        
        db.session.commit()

        return redirect(url_for('doctor_dashboard'))
    else:
        return render_template('update_history.html',app=app)
    

@app.route('/doctor_dashboard/mark_as_done/<int:id>')
def mark_as_done(id):
    app = Appointments.query.filter_by(id=id).first()
    app.app_status = "Completed"

    avail = DoctorAvailability.query.filter_by(doctor_id=app.doctor_id,date=app.app_date).first()

    if avail:
        if app.app_time == time(8, 0, 0):
            avail.morning_slot = True
        elif app.app_time == time(16, 0, 0):  
            avail.evening_slot = True

    db.session.commit()

    return redirect(url_for('doctor_dashboard'))

@app.route('/doctor_dashboard/cancel_appointment/<int:id>')
@app.route('/patient_dashboard/cancel_appointment/<int:id>')
@app.route('/admin_dashboard/cancel_appointment/<int:id>')
def cancel_appointment(id):
    app = Appointments.query.filter_by(id=id).first()
    app.app_status="Canceled"
    

    avail = DoctorAvailability.query.filter_by(doctor_id=app.doctor_id,date=app.app_date).first()

    if avail:
        if app.app_time == time(8, 0, 0):
            avail.morning_slot = True
        elif app.app_time == time(16, 0, 0):  
            avail.evening_slot = True

    db.session.commit()

    if (session['role']=="doctor"):
        return redirect(url_for('doctor_dashboard'))
    elif (session['role']=="patient"):
        return redirect(url_for('patient_dashboard'))
    elif (session['role']=="admin"):
        return redirect(url_for('admin_dashboard'))

@app.route('/doctor_dashboard/patient_history/<int:id>')
def patient_history(id):
    patient_info = Appointments.query.filter_by(patient_id=id).first()
    appointments = Appointments.query.filter_by(patient_id=id,app_status="Completed").all()
    
    
    return render_template('patient_history.html',appointments=appointments,pat=patient_info)

@app.route
@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login'))

@app.route('/admin_dashboard/edit/<int:id>',methods=["GET","POST"])
def edit_doctor(id):
    doctor = User.query.filter_by(id=id).first()

    if request.method=="POST":
        name = request.form['username']
        mail = request.form['email']
        spl_id = request.form['spl_id']
        id = doctor.id
        pwd = doctor.password

        doctor.username = name
        doctor.email = mail
        doctor.spl_id = spl_id

        db.session.commit()

        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('edit_doctor.html',doctor=doctor)
    
@app.route('/admin_dashboard/edit_patient/<int:id>',methods=["GET","POST"])
def edit_patient(id):
    p = User.query.filter_by(id=id).first()

    if request.method=="POST":
        name = request.form['username']
        mail = request.form['email']
        pwd = request.form['password']
        

        p.username = name
        p.email = mail
        p.password = pwd

        db.session.commit()

        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('edit_patient.html',p=p)


@app.route('/admin_dashboard/blacklist/<int:id>')
def blacklist(id):
    user = User.query.filter_by(id=id).first()

    user.blacklisted = not user.blacklisted

    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/doctor_dashboard/availability',methods=["GET","POST"])
def availability():
    dayss = []
    dayss.append(datetime.date.today())

    for i in range(1,7):
        dayss.append(dayss[0] + datetime.timedelta(days=i))

    if request.method=="POST":
        m = request.form.getlist('morning_slot')
        e = request.form.getlist('evening_slot')

        print(m)
        print(e)

        for d in dayss:
            stat=0
            date_obj = datetime.datetime.strptime(str(d), "%Y-%m-%d").date()
            avl = DoctorAvailability.query.filter_by(doctor_id=session['id'],date=date_obj).first()

            if (avl):
                stat=1
                pass
            else:
                avl = DoctorAvailability(doctor_id=session['id'],date=date_obj)

            avl.morning_slot = False
            avl.evening_slot = False

            if str(d) in m:
                avl.morning_slot = True
            if str(d) in e:
                avl.evening_slot = True

            if (stat):
                pass
            else:
                db.session.add(avl)

            db.session.commit()

        return redirect(url_for('doctor_dashboard'))
    else:
        return render_template('doctor_availability.html',days=dayss)

@app.route('/patient_dashboard/department/book_appointment/<int:doc_id>',methods=["GET","POST"])
def book(doc_id):
    dayss = []
    dayss.append(datetime.date.today())
    doc_avail = DoctorAvailability.query.filter_by(doctor_id=doc_id).all()

    for i in range(1,7):
        dayss.append(dayss[0] + datetime.timedelta(days=i))

    if request.method=="POST":
        m = request.form.getlist('morning_slot')
        e = request.form.getlist('evening_slot')

        if len(m)!=0:
            date_str = m[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            app = Appointments(doctor_id=doc_id,app_date=date_obj,app_time=time(8,0),app_status="Assigned",patient_id=session['id'])
            db.session.add(app)
            db.session.commit()

            availb = DoctorAvailability.query.filter_by(doctor_id=doc_id,date=date_obj).first()
            availb.morning_slot = False
            
            db.session.commit()


        if len(e)!=0:
            date_str = e[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            app = Appointments(doctor_id=doc_id,app_date=date_obj,app_time=time(16,0),app_status="Assigned",patient_id=session['id'])
            db.session.add(app)
            db.session.commit()

            availb = DoctorAvailability.query.filter_by(doctor_id=doc_id,date=date_obj).first()
            availb.evening_slot = False

            db.session.commit()

        return redirect(url_for('patient_dashboard'))
    else:
        return render_template('book_appointment.html',days=dayss,doc_avail=doc_avail)


if __name__=='__main__':
    with app.app_context():
        db.create_all()
        initialize_database()

    app.run(debug=True)





