# dotenv-azd

[![PyPI - Version](https://img.shields.io/pypi/v/dotenv-azd.svg)](https://pypi.org/project/dotenv-azd)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotenv-azd.svg)](https://pypi.org/project/dotenv-azd)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install dotenv-azd
```

## Usage

Create a new AZD env if you don't have one yet:

```
azd env new
```

In your Python code:
```
from dotenv_azd import load_azd_env
from os import getenv

load_azd_env()
print(getenv('AZURE_ENV_NAME'))
```

## License

`dotenv-azd` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
