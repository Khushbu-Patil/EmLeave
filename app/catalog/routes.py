from app.catalog import main
from app import db
from app.auth.models import Leave, Registration, Event, Notice
from app.auth.routes import do_the_login, session
from flask import render_template





@main.route('/em_home')
def em_home():
    notice = Notice.query.all()
    return render_template('em_home.html', notice=notice)


@main.route('/ad_home')
def ad_home():
    notice = Notice.query.all()
    return render_template('ad_home.html', notice=notice)

@main.route('/off_home')
def off_home():
    notice = Notice.query.all()
    return render_template('off_home.html', notice=notice)

@main.route('/admin_leave', methods=['GET','POST'])
def display_Admin_Leave():
    userleave = Leave.query.all()
    return render_template('ad_leave.html', employeeleave=userleave)

@main.route('/display_leave/<em_id>', methods=['GET','POST'])
def display_Leave(em_id):
    leave = Leave.query.filter_by(em_id=em_id).all()
    return render_template('display_leave.html', employeeleave=leave)

@main.route('/display_off_leave', methods=['GET','POST'])
def display_off_Leave():
    leave = Leave.query.all()
    return render_template('display_off_leave.html', employeeleave=leave)


@main.route('/display_off_event', methods=['GET','POST'])
def display_off_event():
    event = Event.query.all()
    return render_template('off_event.html', event=event)


@main.route('/display_em_event', methods=['GET','POST'])
def display_em_event():
    event = Event.query.all()
    return render_template('em_event.html', event=event)