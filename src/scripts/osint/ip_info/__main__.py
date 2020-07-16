from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from src.scripts.osint.ip_info.get_ip_info import get_ip_info


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__) -> None:
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        response = get_ip_info(kwargs.get('ip'))

        if type(response) == dict:
            msg = 'Query successful!' if response['status'] == 'success' else 'Query failed!'
            response.pop('status', None)  # we don't need duplicate status, let's get rid of it

            result = ScriptResponse.success(result=response, message=msg)
        else:
            result = ScriptResponse.error(result=response, message='Error occurred while trying to get data!')

        return result
