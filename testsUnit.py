import unittest
import json
import sched.app as app
import sched.models as models
import sched.forms as forms
import sched.filters as filters
from datetime import datetime, date, timedelta
from datetime import timedelta
from jinja2 import Environment


class testModelApponintment(unittest.TestCase):

    def test_appointment_Duration(self):
        now = datetime.now()
        appt = models.Appointment(
            title='Prueba Unitaria', start=now,
            end=now + timedelta(seconds=1800),
            allday=False)
        self.assertEqual(1800, appt.duration)
        self.assertNotEqual(1801, appt.duration)

    def test_appointment_Repre_(self):
        now = datetime.now()
        appt = models.Appointment(
            title='Prueba Unitaria Repre', start=now,
            end=now + timedelta(seconds=1800),
            allday=False)
        self.assertNotEqual('<Appointment: 3>', appt.__repr__())


class testModelUser(unittest.TestCase):

    def test_user_password(self):
        user = models.User(name="Usuario Nuevo", email="email2@cimat.mx")
        user._set_password("thepassword")
        assert "sha1" in user._get_password()        
        self.assertNotEqual(user._get_password(), "thepassword") 
        self.assertEqual(True, user.check_password("thepassword"))
        self.assertNotEqual(True, user.check_password("thepassword2"))
        self.assertEqual(False, user.check_password(""))
    
    
    def test_user_password_none(self):
        user = models.User(name="Usuario Nuevo", email="email@cimat.mx")
        self.assertEqual(False, user.check_password("thepassword"))
        

    def test_user_status(self):
        user = models.User(name="Usuario Nuevo", email="email2@cimat.mx")
        user._set_password("thepassword")
        self.assertNotEqual(user.get_id(), 0)
        self.assertNotEqual(user.is_active(), False)
        self.assertNotEqual(user.is_anonymous(), True)
        self.assertNotEqual(user.is_authenticated(), False)

    def test_user_authenticate(self):
        user, authenticate = models.User.authenticate(
            app.db.session.query, "email@cimat.mx", "thepassword")
        self.assertNotEqual(authenticate, False)
        self.assertNotEqual(user.name, "Usuario")

    def test_user_nonexistent_authenticate(self):
        user, authenticate = models.User.authenticate(
            app.db.session.query, "carlos@cimat.mx", "thepassword")
        self.assertEqual(authenticate, False)
        self.assertEqual(user, None)

    def test_user_noactive_authenticate(self):
        user, authenticate = models.User.authenticate(
            app.db.session.query, "email3@cimat.mx", "thepassword")
        self.assertEqual(authenticate, False)
        self.assertEqual(user.name, "Usuario no activo")


class testForm(unittest.TestCase):

    def test_form_Appt(self):
        form = forms.AppointmentForm()
        self.assertEqual(
            '<input id="title" name="title" type="text" value="">', str(form.title))
        self.assertEqual(
            '<input id="start" name="start" type="text" value="">', str(form.start))
        self.assertEqual(
            '<input id="end" name="end" type="text" value="">', str(form.end))
        self.assertEqual(
            '<input id="allday" name="allday" type="checkbox" value="y">', str(form.allday))
        self.assertEqual(
            '<input id="location" name="location" type="text" value="">', str(form.location))
        self.assertEqual(
            '<textarea id="description" name="description"></textarea>', str(form.description))

    def test_form_Login(self):
        form = forms.LoginForm()
        self.assertEqual(
            '<input id="username" name="username" type="text" value="">', str(form.username))
        self.assertEqual(
            '<input id="password" name="password" type="password" value="">', str(form.password))


class testApp(unittest.TestCase):

    def setUp(self):
        self.appt = app.app.test_client()


    def test_appt_list(self):
        response = self.appt.get("/appointments")
        self.assertEquals(response.status_code, 301)
        assert 'Redirecting' in response.data

    def test_login(self):
        response = self.appt.get("/login/")        
        self.assertEquals(response.status_code, 200)
        assert 'Log user' in response.data        
        response2 = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        self.assertEquals(response2.status_code, 200)
        
    def test_incorrect_login(self):
        response = self.appt.post('/login/', data=dict(
                                    username='carlos@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        self.assertEquals(response.status_code, 200)

    
    def test_logout(self):
        response = self.appt.get("/logout/")        
        self.assertEquals(response.status_code, 302)
        assert 'Redirecting' in response.data

    def test_appoitment_detail(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/appointments/1/')
        self.assertEquals(response.status_code, 200)
        assert "Titulo Nuevo" in response.data
        assert "Ir al dentista" not in response.data

    def test_nonexist_appoitment_detail(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/appointments/0/')
        self.assertEquals(response.status_code, 404)
        assert "Not Found" in response.data

    def test_appoitnment_edit(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/appointments/1/edit/')
        self.assertEquals(response.status_code, 200)        
        assert "Edit Appointment" in response.data
        assert "Add Appointment" not in response.data

        response = self.appt.post('/appointments/1/edit/', data=dict(
                                    title="Titulo Nuevo",
                                    start="2014-10-08 12:38:26",
                                    end="2014-09-30 14:30:27",
                                    location="the office",
                                    description="something text"
                                    ), follow_redirects=True)
        self.assertEquals(response.status_code, 200)        
        assert "Titulo Nuevo" in response.data
        assert "Ir al dentista" not in response.data

    def test_nonexist_appoitnment_edit(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/appointments/0/edit/')        
        self.assertEquals(response.status_code, 404)
        assert "Not Found" in response.data


    def test_appoitnment_create(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/appointments/create/')
        self.assertEquals(response.status_code, 200)        
        assert "Add Appointment" in response.data
        assert "Edit Appointment" not in response.data

        response = self.appt.post('/appointments/create/', data=dict(
                                    title="Una cita nueva",
                                    start="2014-10-08 12:38:26",
                                    end="2014-09-30 14:30:27",
                                    location="the office",
                                    description="something text"
                                    ), follow_redirects=True)
        self.assertEquals(response.status_code, 200)        
        assert "Una cita nueva" in response.data

    def test_appoitnment_delete(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/appointments/1/delete/')
        self.assertEquals(response.status_code, 405)
        assert "Not Allowed" in response.data        

        response = self.appt.delete('/appointments/8/delete/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'status': 'OK'})
        
        response = self.appt.delete('/appointments/33/delete/', follow_redirects=True)        
        self.assertEquals(response.status_code, 404)
        assert "Not Found" in response.data        

    def test_index(self):
        response = self.appt.post('/login/', data=dict(
                                    username='email@cimat.mx',
                                    password='thepassword'), follow_redirects=True)        
        
        response = self.appt.get('/')
        self.assertEquals(response.status_code, 200)        
        assert "Appointment scheduler" in response.data
        
        



class test_filter(unittest.TestCase):
    
    def test_datetime_without_hour(self):
        now = date(2010, 11, 11)
        fecha = filters.do_datetime(now)
        self.assertNotEqual(fecha, "2010-11-11 - Thursday")

    def test_datetime_with_hour(self):
        now = datetime(2010, 11, 11, 13, 00, 00)
        fecha = filters.do_datetime(now)
        self.assertEqual(fecha, '2010-11-11 - Thursday at 1:00pm')

    def test_datetime_None(self):
        fecha = filters.do_datetime(None)
        self.assertNotEqual(fecha, "Today")
        self.assertEqual(fecha, '')


    def test_datetime_format_None(self):
        now = datetime(2010, 11, 11, 14, 00, 00)
        fecha = filters.do_datetime(now, None)
        self.assertEqual(fecha, '2010-11-11 - Thursday at 2:00pm')

    def test_datetime_with_format(self):
        a = '%Y-%m-%d - %A'
        now = datetime(2010, 11, 11, 14, 00, 00)
        fecha = filters.do_datetime(now, a)
        self.assertNotEqual(fecha, '2010-11-11 - Thursday at 2:00pm')

    def test_date_none(self):
        fechadate = filters.do_date(None)
        self.assertEqual(fechadate, '')

    def test_date_not_none(self):
        now = datetime(2010, 11, 11, 13, 00, 00)
        fechadate = filters.do_date(now)
        self.assertNotEqual(fechadate, '2010-11-11 - Thursday at 1:00pm')
        self.assertEqual(fechadate, '2010-11-11 - Thursday')

    def test_duration_hour(self):
        time = filters.do_duration(3600)
        self.assertNotEqual(time, "1 day")
        self.assertEqual(time, "0 day, 1 hour, 0 minute, 0 second")

    def test_duration_days(self):
        time = filters.do_duration(258732)
        self.assertEqual(time, "2 days, 23 hours, 52 minutes, 12 seconds")


    def test_do_nl2br_without_Markup(self):
        template_env = Environment(
          autoescape=False,
         extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
        text = "Texto con '\n' para saltos '\n' pero junto"
        changes = filters.do_nl2br(template_env, text)
        self.assertNotEqual(changes, "")
        self.assertEqual(changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero junto")

    def test_do_nl2br_with_Markup(self):
        template_env = Environment(
          autoescape=True,
         extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
        text = "Texto con '\n' para saltos '\n' pero <script>junto</script>"
        changes = filters.do_nl2br(template_env, text)
        self.assertNotEqual(changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero junto")
        self.assertEqual(changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero &lt;script&gt;junto&lt;/script&gt;")


        
class testDelete(unittest.TestCase):
    pass

# def test_error_delete(self):
#   self.assertRaises(NotImplementedError, m.appointment_delete, 1)

if __name__ == '__main__':
    unittest.main()
