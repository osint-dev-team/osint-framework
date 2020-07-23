#!/usr/bin/env python3

import platform
from pathlib import Path
from time import sleep
from typing import Tuple

import phonenumbers
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Constants:
    # necessary urls
    BASE_URL: str = 'https://vk.com/join'
    FINISH_URL: str = 'https://vk.com/join?act=finish'

    # full name
    FIRST_NAME: str = 'John'
    LAST_NAME: str = 'Smith'

    # birthdate id is used to select necessary items in dropdown lists
    BIRTHDATE: str = '2'


class Defaults:
    # maximum timeout
    MAX_TIMEOUT: float = 10.


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__) -> None:
        super(Runner, self).__init__(logger)
        self.__driver: webdriver = webdriver.Chrome(executable_path=self.__get_driver_path(),
                                                    options=self.__get_driver_options())

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        try:
            country_code, phone_number = self.__split_phone_number(kwargs.get('phone'))
        except Exception as e:
            return ScriptResponse.success(message=str(e))

        self.__driver.get(Constants.BASE_URL)

        # fill the first name and the last name
        self.__fill_form_field((By.ID, 'ij_first_name'), Constants.FIRST_NAME)
        self.__fill_form_field((By.ID, 'ij_last_name'), Constants.LAST_NAME)

        # let's fill the birthdate. First, we need to click the dropdown button and then we can select necessary item
        # dropdown list for day selection has id="dropdown1", for month selection has id="dropdown2", for year selection
        # has id="dropdown3". We will choose the first element in every list.
        for i in range(1, 4):
            self.__click_elem((By.ID, 'dropdown{}'.format(i)))
            self.__click_elem((By.ID, 'option_list_options_container_{}_{}'.format(i, Constants.BIRTHDATE)))

        # sometimes gender option doesn't appear. We need to click submit button and wait
        self.__click_elem((By.ID, 'ij_submit'))
        self.__click_elem((By.CSS_SELECTOR, "div[role='radio']"))
        self.__click_elem((By.ID, 'ij_submit'))

        # we need to wait for url to change and for page to load
        WebDriverWait(self.__driver, Defaults.MAX_TIMEOUT).until(ec.url_changes(Constants.FINISH_URL))
        sleep(1)

        # we need to choose necessary country code
        # first, we need to click dropdown button to get access to all VK country codes
        self.__click_elem((By.ID, 'dropdown1'))

        # wait for list of codes to appear
        WebDriverWait(self.__driver, Defaults.MAX_TIMEOUT).until(ec.visibility_of_element_located(
            (By.ID, 'list_options_container_1')))
        phone_codes = self.__driver.find_element_by_id('list_options_container_1').find_elements_by_tag_name('li')

        for code in phone_codes:
            if country_code in code.text:
                code.click()
                break

        self.__fill_form_field((By.ID, 'join_phone'), phone_number)
        self.__click_elem((By.ID, 'join_send_phone'))
        sleep(1)

        try:
            WebDriverWait(self.__driver, Defaults.MAX_TIMEOUT).until(ec.presence_of_element_located(
                (By.ID, 'join_called_phone')))

            self.__driver.quit()
            return ScriptResponse.success(message='There is a user with such phone number!')
        except TimeoutException:
            self.__driver.quit()
            return ScriptResponse.success(message='User with such phone number doesn\'t exist!')

    @staticmethod
    def __get_driver_path() -> str:
        """
        A method that returns path to chromedriver (with considering OS).

        :return: path to chromedriver.
        """

        return str(Path().resolve() / 'web_drivers' / ('chromedriver_' + platform.system().lower()))

    @staticmethod
    def __get_driver_options():
        options: webdriver.chrome.options.Options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        return options

    def __fill_form_field(self, locator: Tuple[str, str], value, max_timeout: float = Defaults.MAX_TIMEOUT,
                          expectation_condition: callable = ec.presence_of_element_located) -> None:
        """
        A safe method to fill form field. It uses expectation condition to check if element is ready for interaction.

        :param locator: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :param value: value to be put into form.
        :param max_timeout: maximum timeout in seconds.
        :param expectation_condition: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :return: None
        :raises: TimeoutException: thrown when a command does not complete in enough time.
        """

        field = WebDriverWait(self.__driver, max_timeout).until(expectation_condition(locator))
        field.send_keys(value)

    def __click_elem(self, locator: Tuple[str, str], max_timeout: float = Defaults.MAX_TIMEOUT,
                     expectation_condition: callable = ec.element_to_be_clickable) -> None:
        """
        A safe method to click on element. It uses expectation condition to check if element is ready for interaction.

        :param locator: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :param max_timeout: maximum timeout in seconds.
        :param expectation_condition: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :return: None
        :raises: TimeoutException: thrown when a command does not complete in enough time.
        """

        elem = WebDriverWait(self.__driver, max_timeout).until(expectation_condition(locator))
        elem.click()

    @staticmethod
    def __split_phone_number(phone_number):
        try:
            pn = phonenumbers.parse(phone_number)
        except phonenumbers.NumberParseException as err_parse:
            raise phonenumbers.NumberParseException('Invalid phone number!') from err_parse

        if not phonenumbers.is_valid_number(pn):
            raise ValueError('Invalid phone number!')

        return '+' + str(pn.country_code), str(pn.national_number)
