# OSINT Framework

[![Required OS](https://img.shields.io/badge/OS-Linux%20based-blue)](https://en.wikipedia.org/wiki/Linux)
[![Python3 Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--2.0-blue)](/LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)
[![Last Commit](https://img.shields.io/github/last-commit/osint-dev-team/osint-framework)](https://github.com/osint-dev-team/osint-framework)

<p align="center">
    :fork_and_knife: All-in-one OSINT/RECON Swiss Knife
</p>

<p align="center">
  <img src="/assets/screenshots/logo.png?raw=true" alt="OSINT Framework Logo" width="50%" height="50%" />
</p> 

## Screenshots

<div align="center">
  <img src="/assets/screenshots/cli.png?raw=true" alt="OSINT Framework CLI interface">
  <p align="center"><i>CLI interface</i></p>
</div> 


## Installing
### General
```bash
virtualenv -p python3 venv (or python3 -m venv venv)
source venv/bin/activate
# see "macOS Prerequisites" if required
pip3 install -r requirements.txt
```
### macOS Prerequisites
For macOS, additional pre-steps after venv activation are required. Install postgresql and cryptographic dependencies:  
```bash
brew install postgresql pkg-config libffi
brew link openssl
```
Set the following paths based on the "link" command output and libffi installation notes:  
```bash
For compilers to find openssl@1.1 you may need to set:
  export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
  export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"
```
```bash
For compilers to find libffi you may need to set:
  export LDFLAGS="-L/usr/local/opt/libffi/lib"
  export CPPFLAGS="-I/usr/local/opt/libffi/include"
```
You need to combine these flags together and execute the following commands:
```bash
export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib -L/usr/local/opt/libffi/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include -I/usr/local/opt/libffi/include"
```
Also, install `wheel` to build `pycares` in the `venv` environment:
```
pip3 install wheel
```

## Testing
```bash
make tests
```

## Running
### As a framework
To run the framework with a command-line interface:
```bash
python3 cli.py -h
```
### As a REST API web service

<div align="center">
  <img src="/assets/screenshots/docker.png?raw=true" alt="OSINT Framework Docker usage">
</div> 

To run the framework as a web service via docker and docker-compose:  
```bash
make up_log
```
or
```bash
docker-compose up --scale consumer=5
```
## As a separated module
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

## REST API web service usage
1. Create the task:
```http
POST /api/tasks/create HTTP/1.1
Host: localhost:8888
Content-Type: application/json

[
    {
        "case": "base",
        "name": "testname-profile",
        "description": "Base example for 'testname' user profile",
        "kwargs": {
            "username": "testname",
            "email": "testmail@gmail.com",
            "fullname": "Test Name"
        }
    },
    {
        "case": "osint",
        "name": "johndoe-profile",
        "description": "Osint example for 'johndoe' user profile",
        "kwargs": {
            "username": "johndoe",
            "email": "johndoe@gmail.com",
            "fullname": "John Doe"
        }
    },
    {
        "case": "recon",
        "name": "facebook-website",
        "description": "Recon example for 'facebook.com' website",
        "kwargs": {
            "url": "https://facebook.com"
        }
    },
    {
        "case": "recon",
        "name": "vk-website",
        "description": "Recon example for 'vk.com' website",
        "kwargs": {
            "url": "https://vk.com"
        }
    },
    {
        "case": "recon",
        "name": "mail-website",
        "description": "Recon example for 'mail.ru' website",
        "kwargs": {
            "url": "https://mail.ru"
        }
    },
    {
        "case": "recon",
        "name": "8-8-8-8-host",
        "description": "Recon example for '8.8.8.8' host",
        "kwargs": {
            "ip": "8.8.8.8"
        }
    },
    {
        "case": "recon",
        "name": "92-63-64-162-host",
        "description": "Recon example for '92.63.64.162' host",
        "kwargs": {
            "ip": "92.63.64.162"
        }
    },
    {
        "case": "recon",
        "name": "13-91-95-74-host",
        "description": "Recon example for '13.91.95.74' host",
        "kwargs": {
            "ip": "13.91.95.74"
        }
    },
    {
        "case": "recon",
        "name": "87-240-190-78-host",
        "description": "Recon example for '87.240.190.78' host",
        "kwargs": {
            "ip": "87.240.190.78"
        }
    },
    {
        "case": "osint",
        "name": "phone-check",
        "description": "check information about the phone number",
        "kwargs": {
            "phone": 89138111111
        }
    }
]
```
2. Check tasks status:
```http
GET /api/tasks/list HTTP/1.1
Host: localhost:8888
```
3. Get the results when the task is done:
```http
GET /api/results?task_id=<YOUR_TASK_ID> HTTP/1.1
Host: localhost:8888
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
