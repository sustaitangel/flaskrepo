import unittest
from jinja2 import Environment
from sched import app
from sched import models
from sched import forms
from sched import filters
from datetime import datetime
from datetime import timedelta


class pruebaApp(unittest.TestCase):

    def setUp(self):
        self.a = app.app.test_client()

    def testLogin(self):
        r1 = self.a.get("/login/")
        self.assertEquals(r1.status_code, 200)
        assert 'Log In' in r1.data
        r2 = self.a.post('/login/',
                         data=dict(username='cimat@cimat.mx',
                                   password='1234'), follow_redirects=True)
        self.assertEquals(r2.status_code, 200)

    def testLoginFailed(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='111'), follow_redirects=True)
        self.assertEquals(r.status_code, 200)

    def testLogOut(self):
        r = self.a.get("/logout/")
        self.assertEquals(r.status_code, 302)
        assert 'Redirecting' in r.data

    def testIndex(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='111'), follow_redirects=True)
        r = self.a.get('/')
        self.assertEquals(r.status_code, 200)
        assert " " in r.data

    def testAppointmentsList(self):
        r = self.a.get("/appointments")
        self.assertEquals(r.status_code, 301)
        assert 'Redirecting' in r.data

    def testAppoitmentDetailNotFound(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='1234'), follow_redirects=True)
        r = self.a.get('/appointments/0/')
        self.assertEquals(r.status_code, 404)
        assert "Not Found" in r.data

    def testAppoitmentDetail(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='1234'), follow_redirects=True)
        r = self.a.get('/appointments/3/')
        self.assertEquals(r.status_code, 200)
        assert "Follow Up" in r.data
        assert "Cita" not in r.data

    def testAppoitnmentEdit(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='1234'), follow_redirects=True)
        r = self.a.get('/appointments/2/edit/')
        self.assertEquals(r.status_code, 200)
        assert "Edit Appointment" in r.data
        assert "Add Appointment" not in r.data
        r = self.a.post('/appointments/2/edit/', data=dict(
            title='Past Meeting',
            start='2014-10-07 12:51:52.084557',
            end='2014-10-13 14:51:52.084557',
            location='The Office', description=""),
            follow_redirects=True)
        self.assertEquals(r.status_code, 200)
        assert "Past Meeting" in r.data
        assert "Cita" not in r.data

    def testAppoitnmentEditNotFound(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='1234'), follow_redirects=True)
        r = self.a.get('/appointments/0/edit/')
        self.assertEquals(r.status_code, 404)
        assert "Not Found" in r.data

    def testAppoitnmentCreate(self):
        r = self.a.post('/login/',
                        data=dict(username='cimat@cimat.mx',
                                  password='1234'), follow_redirects=True)
        r = self.a.get('/appointments/create/')
        self.assertEquals(r.status_code, 200)
        assert "Add Appointment" in r.data
        assert "Edit Appointment" not in r.data
        r = self.a.post('/appointments/create/',
                        data=dict(title="Reunion",
                                  start="2014-10-11 09:25:00",
                                  end="2014-10-11 10:47:32",
                                  location="the office",
                                  description="Importante"),
                        follow_redirects=True)
        self.assertEquals(r.status_code, 200)
        assert "Reunion" in r.data


class testDelete(unittest.TestCase):
    pass


class pruebaUsuario(unittest.TestCase):

    def testPassword1(self):
        user = models.User(
            name="juanis", email="cimat@cimat.mx", password="246")
        self.assertNotEqual(user._get_password(), "111")
        user._set_password("111")
        self.assertEqual(False, user.check_password("hola"))
        self.assertEqual(True, user.check_password("111"))

    def testPassword2(self):
        user = models.User(name="juanis", email="cimat@cimat.mx")
        self.assertEqual(False, user.check_password("1234"))

    def testAuthenticate1(self):
        db = app.db.session.query
        user, a = models.User.authenticate(db, "cimat@cimat.mx", "1234")
        self.assertNotEqual(a, False)
        self.assertNotEqual(user.name, "juanis")

    def testAuthenticate2(self):
        db = app.db.session.query
        user, a = models.User.authenticate(db, "cimat@cimat.mx", "1234")
        self.assertEqual(a, True)
        self.assertEqual(user.name, "luis")

    def testAuthenticate3(self):
        db = app.db.session.query
        user, a = models.User.authenticate(db, "cimat@cimat.mx", "111")
        self.assertEqual(a, False)
        self.assertEqual(user.name, "luis")

    def testAuthenticate4(self):
        db = app.db.session.query
        user, a = models.User.authenticate(db, "cimat1@cimat.mx", "111")
        self.assertEqual(a, False)
        self.assertEqual(user, None)

    def test_user_status(self):
        user = models.User(
            id=2, name="brisia", email="cimat@cimat.mx", password="333")
        self.assertNotEqual(user.get_id(), 2)
        self.assertNotEqual(user.is_active(), False)
        self.assertNotEqual(user.is_anonymous(), True)
        self.assertNotEqual(user.is_authenticated(), False)


class pruebaFilters(unittest.TestCase):

    def testDo_datetimeNone(self):
        fecha = filters.do_datetime(None)
        self.assertEqual(fecha, '')

    def testDo_dateNone(self):
        fecha = filters.do_date(None)
        self.assertEqual(fecha, '')

    def testDo_datetime(self):
        fecha = filters.do_datetime(datetime(1990, 07, 01, 07, 06, 00))
        self.assertEqual(fecha, '1990-07-01 - Sunday at 7:06am')
        self.assertNotEqual(fecha, '1990-07-01')

    def testDo_date(self):
        fecha = filters.do_date(datetime(1990, 07, 01, 07, 06, 00))
        self.assertEqual(fecha, '1990-07-01 - Sunday')
        self.assertNotEqual(fecha, '1990-07-01 - Sunday at 7:06am')

    def testDo_duration(self):
        d = filters.do_duration(259578)
        self.assertEqual(d, '3 days, 0 hour, 6 minutes, 18 seconds')

    def testDo_durationHrMsSs(self):
        d = filters.do_duration(39574)
        self.assertEqual(d, '0 day, 10 hours, 59 minutes, 34 seconds')

    def testDo_durationHMS(self):
        d = filters.do_duration(3661)
        self.assertEqual(d, '0 day, 1 hour, 1 minute, 1 second')

    def testDo_durationMS(self):
        d = filters.do_duration(75)
        self.assertEqual(d, '0 day, 0 hour, 1 minute, 15 seconds')

    def testDo_nl2br(self):
        formato = Environment(
            autoescape=False,
            extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
        txt = "Texto '\n' retorno '\n' texto"
        txt2 = filters.do_nl2br(formato, txt)
        self.assertNotEqual(txt2, "")
        self.assertEqual(
            txt2, "Texto &#39;<br />&#39; retorno &#39;<br />&#39; texto")

    def testDatetimeFormat(self):
        formato = '%Y-%m-%d - %A'
        now = datetime(2014, 10, 13, 06, 10, 00)
        fecha = filters.do_datetime(now, formato)
        self.assertNotEqual(fecha, '2014-10-13 - Monday at 6:10am')

    def testDo_nl2brMarkup(self):
        formato = Environment(autoescape=True,
                              extensions=['jinja2.ext.i18n',
                                          'jinja2.ext.autoescape'])
        t = "Texto '\n' retorno '\n' texto <script>seguido</script>"
        changes = filters.do_nl2br(formato, t)
        self.assertNotEqual(
            changes, "Texto &#39;<br />&#39; retorno &#39;<br />&#39; seguido")
        self.assertEqual(
            changes, "Texto &#39;<br />&#39; retorno &#39;\
            <br />&#39; texto &lt;script&gt;seguido&lt;/script&gt;")


class pruebaForm(unittest.TestCase):

    def testForm(self):
        f = forms.AppointmentForm()
        self.assertEqual(
            '<input id="title" name="title" type="text" value="">',
            str(f.title))
        self.assertEqual(
            '<input id="start" name="start" type="text" value="">',
            str(f.start))
        self.assertEqual(
            '<input id="end" name="end" type="text" value="">',
            str(f.end))
        self.assertEqual(
            '<input id="allday" name="allday" type="checkbox" value="y">',
            str(f.allday))
        self.assertEqual(
            '<input id="location" name="location" type="text" value="">',
            str(f.location))
        self.assertEqual(
            '<textarea id="description" name="description"></textarea>',
            str(f.description))

    def testLogIn(self):
        f = forms.LoginForm()
        self.assertEqual(
            '<input id="username" name="username" type="text" value="">',
            str(f.username))
        self.assertEqual(
            '<input id="password" name="password" type="password" value="">',
            str(f.password))


class pruebaApponintment(unittest.TestCase):

    def testDurationAppointment(self):
        now = datetime.now()
        a = models.Appointment(id=1, title='Past Meeting',
                               start=now - timedelta(days=3, seconds=3600),
                               end=now - timedelta(days=3),
                               allday=False,
                               location='The Office')
        self.assertEqual(3600, a.duration)

    def testReprAppointment(self):
        now = datetime.now()
        a = models.Appointment(id=1, title='Important Meeting',
                               start=now + timedelta(days=3),
                               end=now + timedelta(days=3, seconds=3600),
                               allday=False, location='The Office')
        self.assertEqual('<Appointment: 1>', a.__repr__())


if __name__ == '__main__':
    unittest.main()
