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

    # maximum timeout
    MAX_TIMEOUT: float = 10.


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs):
        phone = kwargs.get('phone')

        return ScriptResponse.success()

    def __load_driver(self):
                