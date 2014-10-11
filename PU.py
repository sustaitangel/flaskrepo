import unittest
from sched import models
from sched import forms
from sched import filters
from datetime import datetime
from datetime import timedelta


class pruebaUsuario(unittest.TestCase):

    def testPassword1(self):
        user = models.User(name="juanis", email="cimat@cimat.mx", password="246")
        self.assertNotEqual(user._get_password(), "111")  
        user._set_password("111")        
        self.assertEqual(False, user.check_password("hola"))
        self.assertEqual(True, user.check_password("111"))

    def testPassword2(self):
        user = models.User(name="juanis", email="cimat@cimat.mx")
        self.assertEqual(False, user.check_password("1234"))

    def testAuthenticate(self):
        db=app.db.session.query
        user, a= models.User.authenticate (db, "cimat@cimat.mx", "1234")
        self.assertNotEqual(a, False)
        self.assertNotEqual(user.name, "juanis")
        

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
        self.assertEqual(d, '3 days, 6 minutes, 18 seconds')


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
