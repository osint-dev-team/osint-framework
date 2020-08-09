# osint-framework
:eyes: All-in-one OSINT/RECON Swiss Knife

## Installing
```bash
virtualenv -p python3 venv
    (or python3 -m venv venv)
pip3 install -r requirements.txt
```

## Running as a framework
_First of all: provide some arguments in the `main.py` file to collect information based on your data (WIP now, will be improved later)_  

To run the framework:
```bash
python3 main.py example_scenario.yaml
```
To run the tests:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

## Running as a separated module
Basic:
```python3
python3 -m src.scripts.<category>.<name> any_arguments_here
```
Example command:
```bash
python3 -m src.scripts.other.user_greeting JohnDoe
```
Example output:
```
{'message': "Successfully finished! (args: (), kwargs: {'username': "
            "'johndoe'})",
 'result': 'Hello, JohnDoe!',
 'status': 'success'}

```

## Create your own script
Use the following structure:  
1. Create your own module directory in the following way:
```
/src/scripts/<choose_your_category_here>/<your_script_name>/<script_files>
```
2. Provide the following structure of your script directory:
```
your_script_name
├── requirements.txt - provide required libraries
├── __init__.py      - use this module to set the default parent directory (you can copy this file from any other script)
├── __main__.py      - use this module to provide some basic interface to use your script as a module (the same as if __name__ == "__main__")
├── module.py        - use this module to describe the basic logic of your module (you can import it in the __main__.py to provide interface)
└── test_module.py   - use this module for unittest tests
```
3. Create the `__init__.py` file. An example of the `__init__.py` boilerplate structure can be seen below:
```python3
import sys
from pathlib import Path

__root_dir = Path(__file__).parents[4]
sys.path.append(str(__root_dir))

```
4. Create the `__main__.py` file. An example of the `__main__.py` boilerplate structure can be seen below:
```python3
#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from .module import Runner

result = run_module(Runner, args=argv, arg_name="username", arg_default="johndoe")
pprint(result)
```
5. Create the module itself. An example of the basic `module.py` file can be seen below:
```python3
#!/usr/bin/env python3

# Import any required runner
# 1. OsintRunner - for OSINT scripts
# 2. ReconRunner - for RECON scripts
# 3. BaseRunner - for out-of-scope scripts ("other")
from src.core.base.osint import OsintRunner, BaseRunner, ReconRunner, PossibleKeys

# Import 'ScriptResponse' to return good responses from the module, like
# 1. ScriptResponse.success - if everything is good
# 2. ScriptResponse.error - if everything is bad
from src.core.utils.response import ScriptResponse

# Validate your named arguments. For example, this validator
# will raise 'KeyError' if you will try to put 'hostname' argument
# into the 'OsintRunner' runner, and so on
from src.core.utils.validators import validate_kwargs

# You can use OsintRunner, ReconRunner or BaseRunner as the base class
class Runner(OsintRunner):
    """
    Basic script example
    """
    
    # Define required arguments here 
    required = ["my_argument"]

    def __init__(self, logger: str = __name__):
        """
        Re-init base class instance with this function.
        Simply put, you need to provide proper logger name
        to the parent class, so please, save this structure for
        the init function.
        :param logger: logger to use (name of _this_ runner by default)
        """
        super(Runner, self).__init__(logger)

    # Validate input arguments (if you need some validation)
    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        The main '.run()' function to run your script. 
        Note: this function is always synchronous, without any
        async/await init. You can use 'asyncio.run(...)' here,
        but don't put any 'async' before function definition
        :param args: args that you provide (not used for now)
        :param kwargs: kwargs that you provide (required to run something!)
        :return: ScriptResponse message (error or success)
        """
        argument = kwargs.get("my_argument", "Arguments were not provided!")
        ...
        return ScriptResponse.success(message=f"Script finished with argument {argument}")
```
6. For `test_module.py` you can use any required tests (as you wish). A test case for your module is required to keep the project clean.
