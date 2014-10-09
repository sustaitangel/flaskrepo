from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sched.models import Base
from flask import abort, jsonify, redirect, render_template
from flask import request, url_for
from sched.forms import AppointmentForm
from sched.models import Appointment
from sched import filters


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'
# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base
filters.init_app(app)


@app.route('/')
def hello():
    """
    >>> hello()
    'Hello, world, i hate you!!!'
    """
    return 'Hello, world, i hate you!!!'


@app.route('/appointments/')
def appointment_list():
    """
    >>> appointment_list()
    'Listing of all appointments we have.'
    """
    # return 'Listing of all appointments we have.'
    # Query: Get all Appointment objects, sorted by date.
    appts = (db.session.query(Appointment).order_by(
        Appointment.start.asc()).all())
    return render_template('appointment/index.html', appts=appts)


@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    """
    >>> appointment_detail(3)
    'Detail of appointment #3.'
    """
    """Provide HTML page with a given appointment."""
    # Query: get Appointment object by ID.
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found.
        abort(404)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    """
    >>> appointment_edit(5)
    'Form to edit appointment #5.'
    """
    # return 'Form to edit appointment #{}.'.format(appointment_id)
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view.
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    """Provide HTML form to create a new appointment."""
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send user back to full appointment list.
        return redirect(url_for('appointment_list'))
    # Either first load or validation error at this point.
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete(appointment_id):
    # raise NotImplementedError('DELETE')
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found, but with simple JSON response.
        response = jsonify({'status': 'Not Found'})
        response.status = 404
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/not_found.html'), 404


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
