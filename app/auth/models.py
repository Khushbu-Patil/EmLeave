from app import db, bcrypt  # from the app package __init__
from datetime import datetime
from flask_login import UserMixin
from app import login_manager



class Admin(UserMixin,db.Model):
    __tablename__ = 'admin'

    Name = db.Column(db.String(25), nullable=False)
    Phone = db.Column(db.String(10), unique=True, nullable=False)
    Email_id = db.Column(db.String(40), unique=True, nullable=False)
    Ad_id = db.Column(db.String(10), nullable=False, primary_key=True)
    Password = db.Column(db.String(10), unique=False, nullable=False)

    @classmethod
    def Ad_user(cls, Name, Phone, Email_id, Ad_id, Password ):
        admin_user = cls(Name = Name,
                   Phone = Phone,
                   Email_id = Email_id,
                   Ad_id = Ad_id,
                   Password = Password #bcrypt.generate_password_hash(Password).decode('utf8')
                   )
        db.session.add(admin_user)
        db.session.commit()
        return admin_user

    def get_id(self):
        return (self.Ad_id)


class Office(UserMixin,db.Model):
    __tablename__ = 'office'

    Name = db.Column(db.String(25), nullable=False)
    Phone = db.Column(db.String(10), unique=True, nullable=False)
    Email_id = db.Column(db.String(40), unique=True, nullable=False)
    Off_id = db.Column(db.String(10), nullable=False, primary_key=True)
    Password = db.Column(db.String(10), unique=False, nullable=False)

    def check_password(self,Password):
        return bcrypt.check_password_hash(self.Password,Password)

    @classmethod
    def Off_user(cls, Name, Phone, Email_id, Off_id, Password):
        office_user= cls(Name = Name,
                   Phone = Phone,
                   Email_id = Email_id,
                   Off_id = Off_id,
                   Password = Password #bcrypt.generate_password_hash(Password).decode('utf-8')
                   )
        db.session.add(office_user)
        db.session.commit()
        return office_user


    def get_id(self):
        return (self.Off_id)



# Registration table TABLE
class Registration(UserMixin, db.Model):
    __tablename__ = 'employee'

    Name = db.Column(db.String(25), nullable=False)
    Phone = db.Column(db.Integer, unique=True, nullable=False)
    Email_id = db.Column(db.String(40), unique=True, nullable=False)
    Department = db.Column(db.String(40), unique=False, nullable=False)
    Designation = db.Column(db.String(40), unique=False, nullable=False)
    Id = db.Column(db.String(10), nullable=False, primary_key=True)
    Password = db.Column(db.String(20), unique=False, nullable=False)


    # def check_password(self,Password):
    #     return bcrypt.check_password_hash(self.Password,Password)

    @classmethod
    def Em_user(cls, Name, Phone, Email_id, Department, Designation, Id, Password):
        user = cls(Name = Name,
                   Phone = Phone,
                   Email_id = Email_id,
                   Department = Department,
                   Designation = Designation,
                   Id = Id,
                   Password = Password #bcrypt.generate_password_hash(Password).decode('utf-8')
                   )
        db.session.add(user)
        db.session.commit()
        return user
    def is_active(self):
        # all users are active
        return True

    def get_id(self):
        return (self.Id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        # False as we do not support annonymity
        return False

@login_manager.user_loader
def load_user(Id):
    return Registration.get_user(Id)

@login_manager.user_loader
def load_user(Ad_id):
    return Office.query.get(int(Ad_id))

@login_manager.user_loader
def load_user(Off_id):
    return Admin.query.get(int(Off_id))



# LEAVE TABLE
class Leave(UserMixin,db.Model):
    __tablename__ = 'leave'

    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(10), nullable=False)
    Department = db.Column(db.String(50), nullable=False)
    Designation = db.Column(db.String(50), nullable=False)
    Leave = db.Column(db.String(400), nullable=False)
    Status = db.Column(db.String(30), nullable=False, default= 'Pending')
    Days = db.Column(db.Integer,nullable=False)
    check = db.Column(db.String(25),nullable=False, default ='No')
    em_date = db.Column(db.DateTime, default=datetime.utcnow())

    # ESTABLISH RELATIONSHIP
    em_id = db.Column(db.String(10), db.ForeignKey('employee.Id'))

    @classmethod
    def leave_user(cls, Name, Phone, Department, Designation, Leave, em_id,Days):
        leavedb = cls(Name=Name,
                   Phone=Phone,
                   Department=Department,
                   Designation=Designation,
                   Leave=Leave,
                   em_id=em_id,
                   Days=Days
                   )
        db.session.add(leavedb)
        db.session.commit()
        return leavedb


class Event(UserMixin,db.Model):
    __tablename__ = 'event'

    Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String(25), nullable=False)
    Category = db.Column(db.String(20), nullable=False)
    Event = db.Column(db.String(400), nullable=False)
    ev_date = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def event(cls,Date, Category, Event):
        eventdb = cls(Date=Date,
                   Category=Category,
                   Event=Event
                   )
        db.session.add(eventdb)
        db.session.commit()


class Notice(UserMixin,db.Model):
    __tablename__ = 'notice'

    Id = db.Column(db.Integer, primary_key=True)
    Notice = db.Column(db.String(400), nullable=False)
    no_date = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def notice(cls,Notice):
        noticedb = cls(Notice=Notice
                   )
        db.session.add(noticedb)
        db.session.commit()
