Feature: Schedule

Scenario: Login user
  Given For acces to the page "http://127.0.0.1:5000/appointments/"
  When I fill the textBox "username" with "cimat@cimat.mx"
  And I fill the textBox "password" with "1234"
  And I get the form

Scenario: Create new appoiment
  Given For acces to the page "http://127.0.0.1:5000/appointments/create"
  When I fill the textBox "title" with "my birthday"
  And I fill the textBox "start" with "1990-07-01 07:06:00"
  And I fill the textBox  "end" with "1990-07-02 00:00:00"
  And I fill the textBox "location" with "My home"
  And I fill the textBox "description" with "today is a great day"
  And And I get the form

Scenario: Detaill appoitment
  Given For acces to the page "http://127.0.0.1:5000/appointments/create/5"
  Then I can see detail of class "appointment-detail" contains "My Appointment"

Scenario: Obtain de error message
  Given For acces to the page "http://127.0.0.1:5000/appointments/10/"
  Then I can see the error message "Not Found"

Scenario: Edit an appoiment
  Given For acces to the page "http://127.0.0.1:5000/appointments/5/edit"
  When I fill the textBox "title" with "New Title"
  And I get the form
  Then I can see detail of class "appointment-detail" contains "New Title"

Scenario: Edit an appoiment
  Given For acces to the page "http://127.0.0.1:5000/appointments/5/edit"
  When I update the textBox "start" with actual date
  And I get the form
  Then I can see detail of class "appointment-detail" contains the actual date

Scenario: Show all appiments
  Given For acces to the page "http://127.0.0.1:5000/appointments"
  Then I can see least "5" appoitments with the class "appointment-detail"

Scenario: Delete an appoitment 
  Given For acces to the page "http://127.0.0.1:5000/appointments/"
  When If choose the appointment named "my birthday"
  And I take a click in the button "appointment-delete-link"
  And For acces to the page "http://127.0.0.1:5000/appointments/" 
  Then I can see detail of class "appointment-detail" no contains "my birthday"
  
