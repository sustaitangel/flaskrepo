Feature: Schedule

Scenario: Login user
  Given For acces to the page "127.0.0.1:5000/appointments"
  I fill the textBox "username" with "cimat@cimat.mx"
  Then I fill the textBox "password" with "1234"
  And I get the form

Scenario: Create new appoiment
  Given For acces to the page "127.0.0.1:5000/appointments/create"
  I fill the textBox "title" with "my birthday"
  Then I fill the textBox "start" with "1990-07-01 07:06:00"
  Then I fill the textBox  "end" with "1990-07-02 00:00:00"
  Then I fill the textBox "location" with "My home"
  Then I fill the textBox "description" with "today is a great day"
  And And I get the form

Scenario: Detaill appoitment
  Given For acces to the page "127.0.0.1:5000/appointments/create/5"
  Then I can see detail of class "appointment-detail" contains "My Appointment"

Scenario: Obtain de error message
  Given For acces to the page "127.0.0.1:5000/appointments/10/"
  Then I can see the error message "Not Found"

Scenario: Edit an appoiment
  Given For acces to the page "127.0.0.1:5000/appointments/1/edit"
  Then I fill the textBox "title" with "New Title"
  And And I get the form
  Then I can see detail of class "appointment-detail" contains "New Title"

Scenario: Show all appiments
  Given For acces to the page "127.0.0.1:5000/appointments"
  I can see least "5" appoitments with the class "appointment-detail"

Scenario: Delete an appoitment 
  Given For acces to the page "127.0.0.1:5000/appointments/1"
  If choose the appointment named "my birthday"
  And I take a click in the button "appointment-delete-link"
  Next I find to "http://127.0.0.1:5000/appointments/" 
  Then I can see detail of class "appointment-detail" no contains "my birthday"
  
