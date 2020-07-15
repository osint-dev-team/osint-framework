from typing import Tuple

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.scripts.osint.social_networks.sn_src.sn_core.global_const import GlobalConstants


class SNChecker:
    def __init__(self, country_code: str, phone_number: str, chrome_driver_path: str, base_url: str) -> None:
        """
        Initialize the base class with some values.

        :param country_code: country code of the phone number.
        :param phone_number: phone number to be searched
        :param chrome_driver_path: path to chromedriver.exe file.
        :param base_url: registration start page URL.
        """

        # we add plus character here to avoid false coincidences in future.
        self._country_code: str = '+' + self.__preprocess(country_code)
        self._phone_number: str = self.__preprocess(phone_number)

        # we need to use English language for correct work
        options: webdriver.chrome.options.Options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        self._driver: webdriver = webdriver.Chrome(chrome_driver_path, options=options)
        self._driver.get(base_url)

    def run(self):
        """
        Base method for checking whether a user with this phone number is registered in VK.

        :raises: NotImplementedError: this method can't be used and requires implementation in subclasses.
        """

        raise NotImplementedError('Implementation is required!')

    @staticmethod
    def __preprocess(s: str) -> str:
        """
        Base method for preprocessing country code and phone number. It performs the following actions:
        - trim
        - remove non-digit characters

        :param s: a value to be preprocessed.
        :return: preprocessed value.
        """

        return ''.join(c for c in s.strip() if c.isdigit())

    def _fill_form_field(self, locator: Tuple[str, str], value, max_timeout: float = GlobalConstants.MAX_TIMEOUT,
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

        field = WebDriverWait(self._driver, max_timeout).until(expectation_condition(locator))
        field.send_keys(value)

    def _click_elem(self, locator: Tuple[str, str], max_timeout: float = GlobalConstants.MAX_TIMEOUT,
                    expectation_condition: callable = ec.element_to_be_clickable) -> None:
        """
        A safe method to click on element. It uses expectation condition to check if element is ready for interaction.

        :param locator: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :param max_timeout: aximum timeout in seconds.
        :param expectation_condition: visit https://selenium-python.readthedocs.io/waits.html for more information.
        :return: None
        :raises: TimeoutException: thrown when a command does not complete in enough time.
        """

        elem = WebDriverWait(self._driver, max_timeout).until(expectation_condition(locator))
        elem.click()
