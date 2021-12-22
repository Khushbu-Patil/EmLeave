from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,NumberRange
from app.auth.models import Registration, Leave, Office, Admin
from wtforms.fields.html5 import DateField
from flask_datepicker import datepicker

def Id_exists(form,field):
    email = Admin.query.filter_by(Ad_id=field.data).first()
    email1 = Office.query.filter_by(Off_id=field.data).first()
    email2 = Registration.query.filter_by(Id=field.data).first()
    if  email or email1 or email2:
        raise ValidationError('Id is already exist')

def Phone_exists(form,field):
    phone = Admin.query.filter_by(Phone=field.data).first()
    phone1 = Office.query.filter_by(Phone=field.data).first()
    phone2 = Registration.query.filter_by(Phone=field.data).first()
    if phone or phone1 or phone2:
        raise ValidationError('Already Exist')

def Email_exists(form,field):
    email = Admin.query.filter_by(Email_id=field.data).first()
    email1 = Office.query.filter_by(Email_id=field.data).first()
    email2 = Registration.query.filter_by(Email_id=field.data).first()
    if email or email1 or email2:
        raise ValidationError('Alredy Exist')

class Registform(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
    Phone = IntegerField('Phone', validators=[DataRequired(),NumberRange(10, message='mobile number contain only 10 integer'), Phone_exists])
    Email_id=StringField('Email', validators=[DataRequired(), Email(), Email_exists])
    Department = SelectField('Department',choices=[ 'CSE', 'Machenical', 'Civil', 'EC', 'Library' ])
    Designation = SelectField('Designation',
                              choices=['HOD', 'Assistant professor', 'Associate Professor', 'Junior Assistant Professor','Librarian', 'Library Assistant', 'Library Attendant', 'Lab Assistant' ])
    Id = StringField('Id', validators=[DataRequired(), Length(4,10), Id_exists])
    Password = PasswordField('Password',validators=[DataRequired(), Length(6), EqualTo('Confirm',message='password must match')])
    Confirm = PasswordField('Comfirm Password', validators=[DataRequired()])
    Submit=SubmitField('Register')

class AdRegistform(FlaskForm):
    Name = StringField('Name :', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
    Phone = IntegerField('Phone :', validators=[DataRequired(),NumberRange(min=10, max=10, message='mobile number contain only 10 integer'),Phone_exists])
    Email_id=StringField('Email :', validators=[DataRequired(), Email(), Email_exists])
    Id = StringField('Id :', validators=[DataRequired(), Length(4,10), Id_exists])
    Password = PasswordField('Password :',validators=[DataRequired(), Length(6,12, message='6 to 12 character are accepted'), EqualTo('Confirm',message='password must match')])
    Confirm = PasswordField('Comfirm Password :', validators=[DataRequired()])
    Submit=SubmitField('Register')

class OffRegistform(FlaskForm):
    Name = StringField('Name :', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
    Phone = IntegerField('Phone :', validators=[DataRequired(),NumberRange(min=10, max=10, message='mobile number contain only 10 integer'), Phone_exists])
    Email_id=StringField('Email :', validators=[DataRequired(), Email(), Email_exists])
    Id = StringField('Id :', validators=[DataRequired(), Length(4,10), Id_exists])
    Password = PasswordField('Password :',validators=[DataRequired(), Length(6,12, message='6 to 12 character are accepted'), EqualTo('Confirm',message='password must match')])
    Confirm = PasswordField('Comfirm Password :', validators=[DataRequired()])
    Submit=SubmitField('Register')

def email_exists(form,field):
    email = Admin.query.filter_by(Email_id=field.data).first()
    email1 = Office.query.filter_by(Email_id=field.data).first()
    email2 = Registration.query.filter_by(Email_id=field.data).first()
    if not email and not email1 and not email2:
        raise ValidationError('Email is not correct')

class forgotform(FlaskForm):
    Email = StringField('Email :', validators=[DataRequired(), Email(), email_exists])
    Submit = SubmitField('Submit')

class otpform(FlaskForm):
    otp= IntegerField('OTP :', validators=[DataRequired()])
    Submit =  SubmitField('Submit')

class resetform(FlaskForm):
    Password = PasswordField('Password :',validators=[DataRequired(), Length(6,12, message='6 to 12 character are accepted'), EqualTo('Confirm',message='password must match')])
    Confirm = PasswordField('Comfirm Password :', validators=[DataRequired()])
    Submit =  SubmitField('Submit')

class LoginForm(FlaskForm):
    Id = StringField('Employee Id', validators=[DataRequired()])
    Password = PasswordField('Password ', validators=[DataRequired()])
    submit = SubmitField('LogIn')



class AdminLoginForm(FlaskForm):
    Ad_id = StringField('Admin Id ', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('LogIn')

class OfficeLoginForm(FlaskForm):
    Off_id = StringField('Office Id', validators=[DataRequired()])
    Password = PasswordField('Password ', validators=[DataRequired()])
    submit = SubmitField('LogIn')

def em_id_exists(form,field):
    em_id = Registration.query.filter_by(Id=field.data).first()
    if not em_id:
        raise ValidationError('id is not correct')

# def em_id_Off_exists(form,field):
#     em_id = Office.query.filter_by(Off_id=field.data).first()
#     if not em_id:
#         raise ValidationError('id is not correct')
# def name_exists(form,field):
#     em_id = Registration.query.filter_by(Id=field.data).first()
#     name = em_id.Name
#     if not name:
#         raise ValidationError('name is not exist')


class LeaveForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
    Phone = StringField('Phone', validators=[DataRequired(), Length(10)])
    Department = SelectField('Department', choices=['CSE', 'Machenical', 'Civil', 'EC', 'Library'])
    Designation = SelectField('Designation',
                              choices=['HOD', 'Assistant professor', 'Associate Professor',
                                       'Junior Assistant Professor', 'Librarian', 'Library Assistant',
                                       'Library Attendant','Lab Assistant'])
    Days = IntegerField('Days', validators=[DataRequired(),NumberRange(min=1, max=30)])
    em_id = StringField('Id', validators=[DataRequired(), Length(4, 10), em_id_exists])
    Leave = TextAreaField('Leave', id="content-area", validators=[DataRequired()])

    Submit = SubmitField('Send')

# class LeaveOfficeForm(FlaskForm):
#     Name = StringField('Name', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
#     Phone = StringField('Phone', validators=[DataRequired(), Length(10)])
#     Department = SelectField('Department', choices=['CSE', 'Machenical', 'Civil', 'EC', 'Library','Office'])
#     Designation = SelectField('Designation',
#                               choices=['HOD', 'Assistant professor', 'Associate Professor',
#                                        'Junior Assistant Professor', 'Librarian', 'Library Assistant',
#                                        'Library Attendant','Office'])
#     Days = IntegerField('Days', validators=[DataRequired(),NumberRange(min=1, max=30)])
#     em_id = StringField('Id', validators=[DataRequired(), Length(4, 10), em_id_Off_exists])
#     Leave = TextAreaField('Leave', id="content-area", validators=[DataRequired()])
#
#     Submit = SubmitField('Send')

class LeaveAdminForm(FlaskForm):
    Status = SelectField('Status', choices=['Pending', 'Approved', 'Rejected'])
    Submit = SubmitField('Send',id="uptade-button")

class Profileform(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
    Phone = StringField('Phone', validators=[DataRequired(), Length(10)])
    Email_id=StringField('Email', validators=[DataRequired(), Email()])
    Department = SelectField('Department',choices=[ 'CSE', 'Machenical', 'Civil', 'EC', 'Library' ])
    Designation = SelectField('Designation',
                              choices=['HOD', 'Assistant professor', 'Associate Professor', 'Junior Assistant Professor','Librarian', 'Library Assistant', 'Library Attendant','Lab Assistant'  ])
    Submit=SubmitField('Update')

class Passwordform(FlaskForm):
    Oldpassword = PasswordField('Old Password',validators=[DataRequired()])
    Password = PasswordField('New Password',validators=[DataRequired(), Length(6), EqualTo('Confirm',message='password must match')])
    Confirm = PasswordField('Comfirm Password',validators=[DataRequired()])
    Submit=SubmitField('Update')



class ProfileAdminform(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(2, 25, message='between 2 to 15 character')])
    Phone = StringField('Phone', validators=[DataRequired(), Length(10)])
    Email_id=StringField('Email', validators=[DataRequired(), Email()])
    Submit=SubmitField('Update')

class Eventform(FlaskForm):
    Date = DateField('Event Date',id="birthday", format='%Y-%m-%d')
    Category = SelectField('Category',choices=[ 'Holiday', 'Meeting', 'Exam' , 'Other event' ])
    Event = StringField('Event',validators=[DataRequired()])
    Submit=SubmitField('Submit')

class Checkform(FlaskForm):
    check = SelectField('Category',choices=[ 'No', 'Yes' ])
    Submit=SubmitField('Submit')


class Noticeform(FlaskForm):
    Notice = TextAreaField('Notice', id="content-area", validators=[DataRequired()])
    Submit=SubmitField('Submit')