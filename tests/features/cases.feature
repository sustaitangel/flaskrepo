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
  Given For acces to the page "http://127.0.0.1:5000/appointments/create/1"

Scenario: Obtain de error message
  Given For acces to the page "http://127.0.0.1:5000/appointments/10/"
  Then I can see the error message "Not Found"

Scenario: Edit an appoiment
  Given For acces to the page "http://127.0.0.1:5000/appointments/5/edit"
  When I fill the textBox "title" with "New Title"
  And I get the form

Scenario: Edit an appoiment
  Given For acces to the page "http://127.0.0.1:5000/appointments/5/edit"
  When I update the textBox "start" with actual date
  And I get the form

Scenario: Show all appiments
  Given For acces to the page "http://127.0.0.1:5000/appointments"

Scenario: Delete an appoitment 
  Given For acces to the page "http://127.0.0.1:5000/appointments/"
  When If choose the appointment named "my birthday"
  And For acces to the page "http://127.0.0.1:5000/appointments/" 
  
