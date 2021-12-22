from flask import render_template, request, flash, redirect, url_for,session,g
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from app.auth.forms import Registform, LoginForm, AdminLoginForm, OfficeLoginForm,LeaveForm, LeaveAdminForm, Profileform, Passwordform, ProfileAdminform,\
    Eventform, Noticeform, Checkform,AdRegistform, forgotform,otpform, resetform,OffRegistform
from app.auth import authentication as at
from app.auth.models import  Registration, Admin, Office, Leave, Event, Notice
from app import bcrypt,db
import smtplib
import random
import os


@at.route('/', methods = ['GET','POST'])
def do_the_admin_login():
    # if session['loggedin']:
    #     flash('You are already logged-in')
    #     return redirect(url_for('main.ad_home'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(Ad_id=form.Ad_id.data).first()

        if not admin or admin.Password != form.Password.data:
            flash('Invalid Credentials, Please try again',category='danger')
            return redirect(url_for('authentication.do_the_admin_login'))
        session['loggedin'] = True
        session['Id'] = admin.Ad_id
        session['Name'] = admin.Name
        # login_user(admin, form.stay_loggedin.data)
        return redirect(url_for('main.ad_home'))
    return render_template('admin-login.html', form=form)


@at.route('/office-login', methods = ['GET','POST'])
def do_the_office_login():
    # if session['loggedin']:
    #     flash('You are already logged-in')
    #     return redirect(url_for('main.off_home'))

    form = OfficeLoginForm()
    if form.validate_on_submit():
        office = Office.query.filter_by(Off_id=form.Off_id.data).first()

        if not office or office.Password != form.Password.data:
            flash('Invalid Credentials, Please try again',category='danger')
            return redirect(url_for('authentication.do_the_office_login'))
        session['loggedin'] = True
        session['Id'] = office.Off_id
        session['Name'] = office.Name
        return redirect(url_for('main.off_home'))
    return render_template('office-login.html', form=form)




@at.route('/forgot',methods=['GET','POST'])
def forgot():
    form = forgotform()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(Email_id=form.Email.data).first()
        employee = Registration.query.filter_by(Email_id=form.Email.data).first()
        office = Office.query.filter_by(Email_id=form.Email.data).first()
        if admin:
            session['Id'] = admin.Ad_id
        elif employee:
            session['Id'] = employee.Id
        elif office:
            session['Id'] = office.Off_id
        email=form.Email.data
        # id.var=admin.Ad_id
        otp = int(''.join([str(random.randint(10000, 99999))]))
        print(otp)
        #  global check

        s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
        s.starttls()
        s.login("emleave21@gmail.com", "ptjiijbznjfrhyuh")
        msg='Em-Leave Dear User, Your OTP is ' +str(otp)
        s.sendmail("emleave21@gmail.com",email,msg)
        forgot.var=int(otp)
        s.quit()
        flash('OTP Successfully send', category='success')
        return redirect(url_for('authentication.otp'))
    return render_template('forgot.html', form=form)


@at.route('/otp', methods=['GET', 'POST'])
def otp():
    form = otpform()
    if form.validate_on_submit():
        check=forgot.var
        otp.var=session['Id']
        print(otp.var)
        print(check)
        if check!=form.otp.data:
            flash('Incorrect')
            return redirect(url_for('authentication.otp'))
        else:
            return redirect(url_for('authentication.ad_reset'))
    return render_template('otp.html', form=form)


@at.route('/ad_reset', methods=['GET', 'POST'])
def ad_reset():
    id=session['Id']
    admin1 = Admin.query.filter_by(Ad_id=id).first()
    employee1 = Registration.query.filter_by(Id=id).first()
    office1 = Office.query.filter_by(Off_id=id).first()
    if admin1:
        verify = Admin.query.get(id)
    elif employee1:
        verify=Registration.query.get(id)
    elif office1:
        verify=Office.query.get(id)

    form = resetform()
    if form.validate_on_submit():
        verify.Password=form.Password.data
        db.session.add(verify)
        db.session.commit()
        flash('Successfully Update',category='success')
        return redirect(url_for('authentication.do_the_admin_login'))
    return render_template('ad_reset.html',form=form)


@at.route('/regist', methods = ['GET','POST'])
def regist():
    employee = Registration.query.all()
    form = Registform()
    if form.validate_on_submit():
        Registration.Em_user(
            Name=form.Name.data,
            Phone=form.Phone.data,
            Email_id=form.Email_id.data,
            Department=form.Department.data,
            Designation=form.Designation.data,
            Id=form.Id.data,
            Password=form.Password.data
        )
        flash('Registration succesful',category='success')
        return redirect(url_for('authentication.regist'))
    return render_template('regist.html',form = form, employee=employee)

@at.route('/off_regist', methods = ['GET','POST'])
def off_register():
    employee = Office.query.all()
    form = OffRegistform()
    if form.validate_on_submit():
        Office.office_user(
            Name=form.Name.data,
            Phone=form.Phone.data,
            Email_id=form.Email_id.data,
            Off_id=form.Id.data,
            Password=form.Password.data
        )
        flash('Registration succesful',category='success')
        return redirect(url_for('authentication.regist'))
    return render_template('off_register.html',form = form, employee=employee)

@at.route('/delete/<delete_id>',methods=['GET','POST'])
def Off_delete(delete_id):
    user = Office.query.get(delete_id)
    db.session.delete(user)
    db.session.commit()
    flash('Succesfully Done', category='success')
    return redirect(url_for('authentication.off_register'))

@at.route('/em_delete/<delete_id>',methods=['GET','POST'])
def em_delete(delete_id):
    user = Registration.query.get(delete_id)
    employee1 = Leave.query.filter_by(em_id=delete_id).first()
    if request.method == 'POST':
        db.session.delete(employee1)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        flash('Succesfully Done', category='success')
    else:
        flash('Unsuccesful',category='danger')
    return redirect(url_for('authentication.regist'))



@at.route('/ad_regist', methods = ['GET','POST'])
def ad_regist():
    employee = Admin.query.all()
    form = AdRegistform()
    if form.validate_on_submit():
        Admin.Ad_user(
            Name=form.Name.data,
            Phone=form.Phone.data,
            Email_id=form.Email_id.data,
            Ad_id=form.Id.data,
            Password=form.Password.data
        )
        flash('Registration succesful',category='success')
        return redirect(url_for('authentication.verify'))
    return render_template('Adregist.html',form = form, employee=employee)

@at.route('/employee-login', methods = ['GET','POST'])
def do_the_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Registration.query.filter_by(Id=form.Id.data).first()

        if not user or user.Password!=form.Password.data:
            flash('Invalid Credentials, Please try again',category='danger')
            return redirect(url_for('authentication.do_the_login'))
        session['loggedin'] = True
        session['Id'] = user.Id
        session['Name'] = user.Name
        # g.User=Registration.query.get(user.Id)
        # g.log=current_user
        return redirect(url_for('main.em_home'))
    return render_template('employee-login.html', form=form)

@at.route('/profile/<Id>', methods=['GET','POST'])
def profile(Id):
    user = Registration.query.get(Id)
    employee = Registration.query.filter_by(Id=Id).all()
    form = Profileform(obj=user)
    if form.validate_on_submit():
        user.Name=form.Name.data
        user.Phone=form.Phone.data
        user.Email_id=form.Email_id.data
        user.Department=form.Department.data
        user.Designation=form.Designation.data
        db.session.add(user)
        db.session.commit()
        flash('Successfully Update',category='success')
        return redirect(url_for('authentication.profile',Id=user.Id))

    return render_template('em_profile.html',form=form, employee=employee)

@at.route('/password/<Id>', methods=['GET', 'POST'])
def Password(Id):
    user = Registration.query.get(Id)
    form = Passwordform()
    if form.validate_on_submit():
        if user.Password == form.Oldpassword.data:
            user.Password=form.Password.data
            db.session.add(user)
            db.session.commit()
            flash('Successfully Update',category='success')
            return redirect(url_for('authentication.profile',Id=user.Id))
        else:
            flash('Old Password is not correct',category='danger')
    return render_template('password.html',form=form)


@at.route('/ad_profile/<Id>', methods=['GET','POST'])
def ad_profile(Id):
    user = Admin.query.get(Id)
    employee = Admin.query.filter_by(Ad_id=Id).all()
    form = ProfileAdminform(obj=user)
    if form.validate_on_submit():
        user.Name=form.Name.data
        user.Phone=form.Phone.data
        user.Email_id=form.Email_id.data
        db.session.add(user)
        db.session.commit()
        flash('Successfully Update',category='success')
        return redirect(url_for('authentication.ad_profile',Id=user.Ad_id))

    return render_template('ad_profile.html',form=form, employee=employee)

@at.route('/ad_password/<Id>', methods=['GET', 'POST'])
def ad_Password(Id):
    user = Admin.query.get(Id)
    form = Passwordform()
    if form.validate_on_submit():
        if user.Password == form.Oldpassword.data:
            user.Password=form.Password.data
            db.session.add(user)
            db.session.commit()
            flash('Successfully Update',category='success')
            return redirect(url_for('authentication.ad_profile',Id=user.Ad_id))
        else:
            flash('Old Password is not correct',category='danger')
    return render_template('ad_password.html',form=form)



@at.route('/off_profile/<Id>', methods=['GET','POST'])
def off_profile(Id):
    user = Office.query.get(Id)
    employee = Office.query.filter_by(Off_id=Id).all()
    form = ProfileAdminform(obj=user)
    if form.validate_on_submit():
        user.Name=form.Name.data
        user.Phone=form.Phone.data
        user.Email_id=form.Email_id.data
        db.session.add(user)
        db.session.commit()
        flash('Successfully Update',category='success')
        return redirect(url_for('authentication.off_profile',Id=user.Off_id))

    return render_template('off_profile.html',form=form, employee=employee)

@at.route('/off_password/<Id>', methods=['GET', 'POST'])
def off_Password(Id):
    user = Office.query.get(Id)
    form = Passwordform()
    if form.validate_on_submit():
        if user.Password == form.Oldpassword.data:
            user.Password=form.Password.data
            db.session.add(user)
            db.session.commit()
            flash('Successfully Update',category='success')
            return redirect(url_for('authentication.off_profile',Id=user.Off_id))
        else:
            flash('Old Password is not correct',category='danger')
    return render_template('off_password.html',form=form)



@at.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('Id', None)
    session.pop('Name', None)
    flash('Succesfully Logged Out')
    return redirect(url_for('authentication.do_the_admin_login'))

@at.route('/leave/<em_id>', methods=['GET','POST'])
def leave_form(em_id):
    form = LeaveForm()
    if form.validate_on_submit():
        if em_id==form.em_id.data:
            Leave.leave_user(
                Name=form.Name.data,
                Phone=form.Phone.data,
                Department=form.Department.data,
                Designation=form.Designation.data,
                em_id=form.em_id.data,
                Days = form.Days.data,
                Leave=form.Leave.data
                )
            flash('Send Succesfully',category='success')
            return redirect(url_for('main.display_Leave', em_id=form.em_id.data))
        else:
            flash('Id is not correct',category='danger')
            redirect(url_for('authentication.leave_form',em_id=em_id))

    return render_template('leave.html', form=form)

# @at.route('/leave_office', methods=['GET','POST'])
# def leave_Office_form():
#     form = LeaveOfficeForm()
#     if form.validate_on_submit():
#         Leave.leave_user(
#             Name=form.Name.data,
#             Phone=form.Phone.data,
#             Department=form.Department.data,
#             Designation=form.Designation.data,
#             em_id=form.em_id.data,
#             Days = form.Days.data,
#             Leave=form.Leave.data
#         )
#         print(form.em_id.data)
#         flash('send succesfully')
#         return redirect(url_for('main.display_office_Leave', em_id=form.em_id.data))
#
#     return render_template('leave_off.html', form=form)

@at.route('/update_leave/<leave_id>', methods=['GET', 'POST'])
def update_leave(leave_id):
    leave = Leave.query.get(leave_id)
    form = LeaveAdminForm(obj=leave)
    if form.validate_on_submit():
        leave.Status = form.Status.data
        db.session.add(leave)
        db.session.commit()
        flash('Successfully Update',category='success')
        return redirect(url_for('main.display_Admin_Leave'))
    return render_template('update_leave.html',form=form)


@at.route('/check/<leave_id>',methods=['GET', 'POST'])
def check(leave_id):
    leave = Leave.query.get(leave_id)
    form = Checkform(obj=leave)
    if form.validate_on_submit():
        leave.check=form.check.data
        db.session.add(leave)
        db.session.commit()
        flash('Successfully Update', category='success')
        return redirect(url_for('main.display_off_Leave'))
    return render_template('update.html', form=form)


@at.route('/event', methods=['GET','POST'])
def ad_event():
    event = Event.query.all()
    form = Eventform()
    if form.validate_on_submit():
        Event.event(
            Date=form.Date.data,
            Category=form.Category.data,
            Event=form.Event.data
        )
        flash('Submit Succesfully',category='success')
        return redirect(url_for('authentication.ad_event'))

    return render_template('ad_event.html', form=form, event=event)

@at.route('/notice', methods=['GET','POST'])
def notice():
    form = Noticeform()
    if form.validate_on_submit():
        Notice.notice(
            Notice=form.Notice.data,
        )
        flash('Submit Succesfully',category='success')
        return redirect(url_for('main.ad_home'))

    return render_template('ad_notice.html', form=form)


