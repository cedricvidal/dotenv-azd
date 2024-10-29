# dotenv-azd

[![PyPI - Version](https://img.shields.io/pypi/v/dotenv-azd.svg)](https://pypi.org/project/dotenv-azd)
![PyPI - Status](https://img.shields.io/pypi/status/dotenv-azd)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotenv-azd.svg)](https://pypi.org/project/dotenv-azd)
![PyPI - Downloads](https://img.shields.io/pypi/dd/dotenv-azd)

This library allows to seamlessly integrate [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/) (azd) environment variables into your Python application without needing to manually export them to an `.env` file.

It uses the `azd` cli and the [python-dotenv](https://pypi.org/project/python-dotenv/) library.

- [Why](#why)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Override Mode](#override-mode)
  - [Quiet Mode](#quiet-mode)
- [License](#license)

## Installation

```console
pip install dotenv-azd
```

## Usage

### Basic Usage

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

## Alternatives

The traditional approach to integrate `azd` environment variables is to export them to a `.env` file and load that file:

```console
azd env get-values > .env
```

This approach can create variable quoting issues and might lead to stale variables when switching between environments using `azd select`.

## License

`dotenv-azd` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
