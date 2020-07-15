from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.core.base.osint import OsintRunner
from src.core.utils.response import ScriptResponse
from src.scripts.osint.social_networks.sn_src.sn_core.global_const import GlobalConstants
from src.scripts.osint.social_networks.sn_src.sn_core.sn_checker import SNChecker
from src.scripts.osint.social_networks.sn_src.vk.vk_const import VKConstants


class VKChecker(SNChecker, OsintRunner):
    def __init__(self, country_code: str, phone_number: str, chrome_driver_path: str) -> None:
        """
        Initialize the class with some values.

        :param country_code: country code of the phone number.
        :param phone_number: phone number to be searched
        :param chrome_driver_path: path to chromedriver.exe file.
        :return: None
        """

        super(VKChecker, self).__init__(country_code, phone_number, chrome_driver_path, VKConstants.BASE_URL)

    def run(self) -> ScriptResponse.error or ScriptResponse.success:
        """
        This method checks if user with provided phone number is registered on VK.

        :return: ScriptResponse message (error or success)
        """
        # fill the first name and the last name
        self._fill_form_field((By.ID, 'ij_first_name'), VKConstants.FIRST_NAME)
        self._fill_form_field((By.ID, 'ij_last_name'), VKConstants.LAST_NAME)

        # let's fill the birthdate. First, we need to click the dropdown button and then we can select necessary item
        # dropdown list for day selection has id="dropdown1", for month selection has id="dropdown2", for year selection
        # has id="dropdown3". We will choose the first element in every list.
        for i in range(1, 4):
            self._click_elem((By.ID, 'dropdown{}'.format(i)))
            self._click_elem((By.ID, 'option_list_options_container_{}_{}'.format(i, VKConstants.BIRTHDATE)))

        # sometimes gender option doesn't appear. We need to click submit button and wait
        self._click_elem((By.ID, 'ij_submit'))
        self._click_elem((By.CSS_SELECTOR, "div[role='radio']"))
        self._click_elem((By.ID, 'ij_submit'))

        # we need to wait for url to change and for page to load
        WebDriverWait(self._driver, GlobalConstants.MAX_TIMEOUT).until(ec.url_changes(VKConstants.FINISH_URL))
        sleep(1)

        # we need to choose necessary country code
        # first, we need to click dropdown button to get access to all VK country codes
        self._click_elem((By.ID, 'dropdown1'))

        # wait for list of codes to appear
        WebDriverWait(self._driver, GlobalConstants.MAX_TIMEOUT).until(ec.visibility_of_element_located(
            (By.ID, 'list_options_container_1')))
        phone_codes = self._driver.find_element_by_id('list_options_container_1').find_elements_by_tag_name('li')

        for code in phone_codes:
            if self._country_code in code.text:
                code.click()
                break

        self._fill_form_field((By.ID, 'join_phone'), self._phone_number)
        self._click_elem((By.ID, 'join_send_phone'))
        sleep(1)

        result = None

        try:
            WebDriverWait(self._driver, GlobalConstants.MAX_TIMEOUT).until(ec.presence_of_element_located(
                (By.ID, 'join_called_phone')))
            error = self._driver.find_element_by_class_name('msg_text')

            if error.find_elements_by_tag_name('b')[0].text.lower() == 'invalid phone number':
                result = ScriptResponse.success(message='Phone number is invalid!')
            else:
                result = ScriptResponse.success(message='There is a user with such phone number!')

        except TimeoutException:
            result = ScriptResponse.success(message='User with such phone number doesn\'t exist!')

        return result
