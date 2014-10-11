
[1;37mFeature: Schedule                                                                 [1;30m# features/cases.feature:1[0m

[1;37m  Scenario: Login user                                                            [1;30m# features/cases.feature:3[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments"                     [1;30m# features/cases.feature:4[0m
[0;33m    I fill the textBox "username" with "cimat@cimat.mx"                           [1;30m# features/cases.feature:5[0m
[0;33m    Then I fill the textBox "password" with "1234"                                [1;30m# features/cases.feature:6[0m
[0;33m    And I get the form                                                            [1;30m# features/cases.feature:7[0m

[1;37m  Scenario: Create new appoiment                                                  [1;30m# features/cases.feature:9[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments/create"              [1;30m# features/cases.feature:10[0m
[0;33m    I fill the textBox "title" with "my birthday"                                 [1;30m# features/cases.feature:11[0m
[0;33m    Then I fill the textBox "start" with "1990-07-01 07:06:00"                    [1;30m# features/cases.feature:12[0m
[0;33m    Then I fill the textBox  "end" with "1990-07-02 00:00:00"                     [1;30m# features/cases.feature:13[0m
[0;33m    Then I fill the textBox "location" with "My home"                             [1;30m# features/cases.feature:14[0m
[0;33m    Then I fill the textBox "description" with "today is a great day"             [1;30m# features/cases.feature:15[0m
[0;33m    And And I get the form                                                        [1;30m# features/cases.feature:16[0m

[1;37m  Scenario: Detaill appoitment                                                    [1;30m# features/cases.feature:18[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments/create/5"            [1;30m# features/cases.feature:19[0m
[0;33m    Then I can see detail of class "appointment-detail" contains "My Appointment" [1;30m# features/cases.feature:20[0m

[1;37m  Scenario: Obtain de error message                                               [1;30m# features/cases.feature:22[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments/10/"                 [1;30m# features/cases.feature:23[0m
[0;33m    Then I can see the error message "Not Found"                                  [1;30m# features/cases.feature:24[0m

[1;37m  Scenario: Edit an appoiment                                                     [1;30m# features/cases.feature:26[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments/1/edit"              [1;30m# features/cases.feature:27[0m
[0;33m    Then I fill the textBox "title" with "New Title"                              [1;30m# features/cases.feature:28[0m
[0;33m    And And I get the form                                                        [1;30m# features/cases.feature:16[0m
[0;33m    Then I can see detail of class "appointment-detail" contains "New Title"      [1;30m# features/cases.feature:30[0m

[1;37m  Scenario: Show all appiments                                                    [1;30m# features/cases.feature:32[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments"                     [1;30m# features/cases.feature:4[0m
[0;33m    I can see least "5" appoitments with the class "appointment-detail"           [1;30m# features/cases.feature:34[0m

[1;37m  Scenario: Delete an appoitment                                                  [1;30m# features/cases.feature:36[0m
[0;33m    Given For acces to the page "127.0.0.1:5000/appointments/1"                   [1;30m# features/cases.feature:37[0m
[0;33m    If choose the appointment named "my birthday"                                 [1;30m# features/cases.feature:38[0m
[0;33m    And I take a click in the button "appointment-delete-link"                    [1;30m# features/cases.feature:39[0m
[0;33m    Next I find to "http://127.0.0.1:5000/appointments/"                          [1;30m# features/cases.feature:40[0m
[0;33m    Then I can see detail of class "appointment-detail" no contains "my birthday" [1;30m# features/cases.feature:41[0m

[1;37m1 feature ([0;31m0 passed[1;37m)[0m
[1;37m7 scenarios ([0;31m0 passed[1;37m)[0m
[1;37m26 steps ([0;33m26 undefined[1;37m, [1;32m0 passed[1;37m)[0m

[0;33mYou can implement step definitions for undefined steps with these snippets:

# -*- coding: utf-8 -*-
from lettuce import step

@step(u'Given For acces to the page "([^"]*)"')
def given_for_acces_to_the_page_group1(step, group1):
    assert False, 'This step must be implemented'
@step(u'I fill the textBox "([^"]*)" with "([^"]*)"')
def i_fill_the_textbox_group1_with_group2(step, group1, group2):
    assert False, 'This step must be implemented'
@step(u'Then I fill the textBox "([^"]*)" with "([^"]*)"')
def then_i_fill_the_textbox_group1_with_group2(step, group1, group2):
    assert False, 'This step must be implemented'
@step(u'And I get the form')
def and_i_get_the_form(step):
    assert False, 'This step must be implemented'
@step(u'Then I fill the textBox  "([^"]*)" with "([^"]*)"')
def then_i_fill_the_textbox_group1_with_group2(step, group1, group2):
    assert False, 'This step must be implemented'
@step(u'And And I get the form')
def and_and_i_get_the_form(step):
    assert False, 'This step must be implemented'
@step(u'Then I can see detail of class "([^"]*)" contains "([^"]*)"')
def then_i_can_see_detail_of_class_group1_contains_group2(step, group1, group2):
    assert False, 'This step must be implemented'
@step(u'Then I can see the error message "([^"]*)"')
def then_i_can_see_the_error_message_group1(step, group1):
    assert False, 'This step must be implemented'
@step(u'I can see least "([^"]*)" appoitments with the class "([^"]*)"')
def i_can_see_least_group1_appoitments_with_the_class_group2(step, group1, group2):
    assert False, 'This step must be implemented'
@step(u'If choose the appointment named "([^"]*)"')
def if_choose_the_appointment_named_group1(step, group1):
    assert False, 'This step must be implemented'
@step(u'And I take a click in the button "([^"]*)"')
def and_i_take_a_click_in_the_button_group1(step, group1):
    assert False, 'This step must be implemented'
@step(u'Next I find to "([^"]*)"')
def next_i_find_to_group1(step, group1):
    assert False, 'This step must be implemented'
@step(u'Then I can see detail of class "([^"]*)" no contains "([^"]*)"')
def then_i_can_see_detail_of_class_group1_no_contains_group2(step, group1, group2):
    assert False, 'This step must be implemented'[0m
