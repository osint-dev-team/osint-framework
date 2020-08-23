#!/usr/bin/env python3

import os
import platform
import stat
from pathlib import Path
from time import sleep
from typing import Callable, Tuple, Any, Optional

import phonenumbers
from phonenumbers import PhoneNumber
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Constants:
    # necessary urls
    BASE_URL: str = "https://vk.com/join"
    FINISH_URL: str = "https://vk.com/join?act=finish"

    # full name
    FIRST_NAME: str = "John"
    LAST_NAME: str = "Smith"

    # birthdate id is used to select necessary items in dropdown lists
    BIRTHDATE: str = "2"


class Defaults:
    # maximum timeout
    MAX_TIMEOUT: float = 10.0


class Runner(OsintRunner):
    """
    Class that performs VK.com registration status (by phone number)
    """

    required = ["phone"]

    def __init__(self, logger: str = __name__) -> None:
        super(Runner, self).__init__(logger)
        try:
            self.__driver: webdriver = webdriver.Chrome(
                executable_path=self.__get_driver_path(),
                options=self.__get_driver_options(),
            )
        except:
            self.__driver: webdriver = webdriver.Chrome(
                executable_path="/usr/bin/chromedriver",
                options=self.__get_driver_options(),
            )

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        try:
            country_code, phone_number = self.__split_phone_number(kwargs.get("phone"))
        except Exception as e:
            return ScriptResponse.success(message=str(e))

        self.__driver.get(Constants.BASE_URL)

        # fill the first name and the last name
        self.__fill_form_field((By.ID, "ij_first_name"), Constants.FIRST_NAME)
        self.__fill_form_field((By.ID, "ij_last_name"), Constants.LAST_NAME)

        # let's fill the birthdate. First, we need to click the dropdown button and then we can select necessary item
        # dropdown list for day selection has id="dropdown1", for month selection has id="dropdown2", for year selection
        # has id="dropdown3". We will choose the first element in every list.
        for i in range(1, 4):
            self.__click_elem((By.ID, "dropdown{}".format(i)))
            self.__click_elem(
                (
                    By.ID,
                    "option_list_options_container_{}_{}".format(
                        i, Constants.BIRTHDATE
                    ),
                )
            )

        # sometimes gender option doesn't appear. We need to click submit button and wait
        self.__click_elem((By.ID, "ij_submit"))
        self.__click_elem((By.CSS_SELECTOR, "div[role='radio']"))
        self.__click_elem((By.ID, "ij_submit"))

        # we need to wait for url to change and for page to load
        WebDriverWait(self.__driver, Defaults.MAX_TIMEOUT).until(
            ec.url_changes(Constants.FINISH_URL)
        )
        self.__wait_page_load()

        # we need to choose necessary country code
        # first, we need to click dropdown button to get access to all VK country codes
        self.__click_elem((By.ID, "dropdown1"))

        # wait for list of codes to appear
        WebDriverWait(self.__driver, Defaults.MAX_TIMEOUT).until(
            ec.visibility_of_element_located((By.ID, "list_options_container_1"))
        )
        phone_codes = self.__driver.find_element_by_id(
            "list_options_container_1"
        ).find_elements_by_tag_name("li")

        for code in phone_codes:
            if country_code in code.text:
                code.click()
                break

        self.__fill_form_field((By.ID, "join_phone"), phone_number)
        self.__click_elem((By.ID, "join_send_phone"))
        self.__wait_page_load()

        try:
            WebDriverWait(self.__driver, Defaults.MAX_TIMEOUT).until(
                ec.presence_of_element_located((By.ID, "join_called_phone"))
            )

            self.__driver.quit()

            return ScriptResponse.success(
                message="There is a user with such phone number!"
            )
        except TimeoutException:
            self.__driver.quit()

            return ScriptResponse.success(
                message="User with such phone number doesn't exist!"
            )

    @staticmethod
    def __set_execution_rights(path: str) -> None:
        """
        A function that sets execution rights to file.

        :param path: path to file.

        :return: None
        """

        st: os.stat_result = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

    def __get_driver_path(self) -> str:
        """
        A method that returns path to chromedriver (with considering OS).

        :return: path to chromedriver.
        """

        system: str = platform.system().lower()
        path: str = str(
            Path(__file__).parent.parent.parent.parent
            / "drivers"
            / (
                "chromedriver_" + system + ".exe"
                if system == "windows"
                else "chromedriver_" + system
            )
        )

        self.__set_execution_rights(path)

        return path

    @staticmethod
    def __get_driver_options() -> Options:
        """
        A function that constructs options for webdriver, such as language and headless mode.

        :return: webdriver options.
        """

        options: Options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        return options

    def __get_page_hash(self) -> int:
        """
        A method that calculates current page's DOM hash.

        :return: DOM hash.
        """

        dom: Optional[Any] = self.__driver.find_elements_by_tag_name("html")[
            0
        ].get_attribute("innerHTML")

        return hash(dom.encode("utf-8"))

    def __wait_page_load(self) -> None:
        """
        A method that waits for page to load.

        :return: None
        """

        page_hash: int = self.__get_page_hash()
        new_page_hash: Optional[int] = None

        while page_hash != new_page_hash:
            page_hash = self.__get_page_hash()
            sleep(Defaults.MAX_TIMEOUT / 100)
            new_page_hash = self.__get_page_hash()

    def __fill_form_field(
        self,
        locator: Tuple[str, str],
        value,
        max_timeout: float = Defaults.MAX_TIMEOUT,
        expectation_condition: Callable = ec.presence_of_element_located,
    ) -> None:
        """
        A safe method to fill form field. It uses expectation condition to check if element is ready for interaction.

        :param locator: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :param value: value to be put into form.
        :param max_timeout: maximum timeout in seconds.
        :param expectation_condition: visit https://selenium-python.readthedocs.io/waits.html for more information.

        :return: None

        :raises: TimeoutException: thrown when a command does not complete in enough time.
        """

        field = WebDriverWait(self.__driver, max_timeout).until(
            expectation_condition(locator)
        )
        field.send_keys(value)

    def __click_elem(
        self,
        locator: Tuple[str, str],
        max_timeout: float = Defaults.MAX_TIMEOUT,
        expectation_condition: Callable = ec.element_to_be_clickable,
    ) -> None:
        """
        A safe method to click on element. It uses expectation condition to check if element is ready for interaction.

        :param locator: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :param max_timeout: maximum timeout in seconds.
        :param expectation_condition: visit https://selenium-python.readthedocs.io/waits.html for more information.

        :return: None

        :raises: TimeoutException: thrown when a command does not complete in enough time.
        """

        elem = WebDriverWait(self.__driver, max_timeout).until(
            expectation_condition(locator)
        )
        elem.click()

    @staticmethod
    def __split_phone_number(phone_number: str) -> Tuple[str, str]:
        """
        A function that splits phone number into country code and national number.

        :param phone_number: phone number in international format.

        :return: a tuple consisting of country code and national number.

        :raises: phonenumbers.NumberParseException: thrown when the attempt to parse the phone number failed.
        :raises: ValueError: thrown when the provided phone number is invalid.
        """

        try:
            pn: PhoneNumber = phonenumbers.parse(phone_number)
        except phonenumbers.NumberParseException as err_parse:
            raise phonenumbers.NumberParseException(
                error_type=phonenumbers.NumberParseException.NOT_A_NUMBER,
                msg="Invalid phone number!",
            ) from err_parse

        if not phonenumbers.is_valid_number(pn):
            raise ValueError("Invalid phone number!")

        return "+" + str(pn.country_code), str(pn.national_number)
