# -*- coding: utf-8 -*-
from lettuce import *
from lettuce_webdriver.util import AssertContextManager
from datetime import datetime
from selenium import webdriver


@before.all
def setup_browser():
    world.browser = webdriver.Firefox()


@after.all
def close_browser(total):
    world.browser.quit()


def find_field_by_class(browser, attribute):
    xpath = "//input[@class='%s']" % attribute
    elems = browser.find_elements_by_xpath(xpath)
    return elems[0] if elems else False


@step('For acces to the page "([^"]*)"')
def given_for_acces_to_the_page_group1(step, url):
    world.response = world.browser.get(url)


@step('I fill the textBox "([^"]*)" with "([^"]*)"')
def when_i_fill_the_textbox_group1_with_group2(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)


@step('I fill the textBox  "([^"]*)" with "([^"]*)"')
def and_i_fill_the_textbox_group1_with_group2(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)


@step('I get the form')
def and_and_i_get_the_form(step):
    with AssertContextManager(step):
        form = world.browser.find_element_by_class_name('form-horizontal')
        form.submit()


@step('I can see detail of class "([^"]*)" contains "([^"]*)"')
def element_contains(step, element_class, value):
    with AssertContextManager(step):
        element = world.browser.find_element_by_class_name(element_class)
        assert (value in element.text), "Got %s, %s " % (element.text, value)


@step('I can see the error message "([^"]*)"')
def then_i_can_see_the_error_message_group1(step, title):
    with AssertContextManager(step):
        element = world.browser.find_element_by_tag_name('h2')
        assert title == element.text, "Got %s " % element.text


@step('I can see detail of class "([^"]*)" contains "([^"]*)"')
def when_i_update(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)

fechaActual = datetime.now().strftime("%Y-%m-%d %l:%M:%S")
fechaActualComparacion = datetime.now().strftime("%Y-%m-%d")


@step('I update the textBox "([^"]*)" with actual date')
def when_i_update_the_textbox_group1_with_actual_date(step, field_id):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(fechaActual)


@step('I can see detail of class"([^"]*)" contains the actual date')
def then_i_can_class_group1_contains_the_actual_date(step, element_class):
    with AssertContextManager(step):
        element = world.browser.find_element_by_class_name(element_class)
        assert fechaActualComparacion in element.text, "Got %s " % element.text


@step('I can see least "([^"]*)" appoitments with the class "([^"]*)"')
def then_it_group1_appoitments_the_class_group2(step, num, element_class):
    with AssertContextManager(step):
        elements = world.browser.find_elements_by_class_name(element_class)
        assert len(elements) > int(num)


@step('If choose the appointment named "([^"]*)"')
def when_if_choose_the_appointment_named_group1(step, title):
    with AssertContextManager(step):
        element = world.browser.find_element_by_link_text(title)
        element.click()


@step('Then I can see detail of class "([^"]*)" not contains "([^"]*)"')
def then_i_can_see_detail_group1_no__group2(step, element_class, title):
    with AssertContextManager(step):
        elements = world.browser.find_elements_by_class_name(element_class)
        lst = []
        for e in elements:
            lst.append(e.text)

        assert title not in lst


@step(u'Then I can see detail of class "([^"]*)" no contains "([^"]*)"')
def then_i_detail_of_class_group1_no_group2(step, group1, group2):
    assert False, 'This step must be implemented'
