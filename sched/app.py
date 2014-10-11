from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sched.models import Base
from flask import abort, jsonify, redirect, render_template
from flask import request, url_for
from sched.forms import AppointmentForm, LoginForm
from sched.models import Appointment
from sched import filters
from flask.ext.login import login_required
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, logout_user
from sched.models import User
# Use Flask-Login to track current user in Flask's session.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'
# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base
filters.init_app(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
app.secret_key = 'que_onda_banda'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User instance from ID."""
    return db.session.query(User).get(user_id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('appointment_list'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()        
        password = form.password.data.lower().strip()       
        user, authenticated = User.authenticate(
            db.session.query, email, password)
        if authenticated:
            login_user(user)
            return redirect(url_for('appointment_list'))
    else:
        error = 'Incorrect username or password.'
    return render_template('user/login.html', form=form, error=error)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def hello():
    """
    >>> hello()
    'Hello, world, i hate you!!!'
    """
    # return 'Hello, world, i hate you!!!'
    return render_template('index.html')


@app.route('/appointments/')
@login_required
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
@login_required
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
    if appt.user_id != current_user.id:
        abort(403)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
@login_required
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
    if appt.user_id != current_user.id:
        abort(403)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view.
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/create/', methods=['GET', 'POST'])
@login_required
def appointment_create():
    """Provide HTML form to create a new appointment."""
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment(user_id=current_user.id)
        # appt = Appointment()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send user back to full appointment list.
        return redirect(url_for('appointment_list'))
    # Either first load or validation error at this point.
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
@login_required
def appointment_delete(appointment_id):
    # raise NotImplementedError('DELETE')
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found, but with simple JSON response.
        response = jsonify({'status': 'Not Found'})
        response.status = 404
        return response
    if appt.user_id != current_user.id:
        response = jsonify({'status': 'Not match User'})
        response.status = 403
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/not_found.html'), 404


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
