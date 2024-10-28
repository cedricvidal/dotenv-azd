# dotenv-azd

[![PyPI - Version](https://img.shields.io/pypi/v/dotenv-azd.svg)](https://pypi.org/project/dotenv-azd)
![PyPI - Status](https://img.shields.io/pypi/status/dotenv-azd)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotenv-azd.svg)](https://pypi.org/project/dotenv-azd)
![PyPI - Downloads](https://img.shields.io/pypi/dd/dotenv-azd)

This library provides a Python [python-dotenv](https://pypi.org/project/python-dotenv/) wrapper function that loads dotenv key value pairs from the currently selected [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/) (azd) environment.

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install dotenv-azd
```

## Usage

Create a new AZD env if you don't have one yet and set an initial variable value:

```console
azd init MY_AZD_ENV
azd env set VAR1 OVERRIDE
```

In your Python code:

```python
from dotenv_azd import load_azd_env
from os import getenv, environ

environ['VAR1'] = 'INITIAL'

load_azd_env()

print(getenv('AZURE_ENV_NAME')) # prints 'MY_AZD_ENV', loaded from azd env

print(getenv('VAR1')) # prints 'INITIAL', was already in Python env
```

### Override mode

You can also override variables in Python env:

```python
load_azd_env(override=True)
print(getenv('VAR1')) # prints 'OVERRIDE', loaded from azd env, overriding Python env
```

### Quiet mode

If you want to ignore errors when `azd` is not initialized or no `azd` environment is active, you can use the `quiet` parameter. This is useful when integrating with `azd` while avoiding dependency on it.

```python
load_azd_env(quiet=True)
```

## License

`dotenv-azd` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
