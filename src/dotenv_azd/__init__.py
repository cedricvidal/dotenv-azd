import subprocess
from os import PathLike
from typing import Optional, TypeAlias

from dotenv import load_dotenv

StrOrBytesPath: TypeAlias = str | bytes | PathLike

def _azd_env_get_values(cwd: Optional[StrOrBytesPath] = None) -> str:
    result = subprocess.run(['azd', 'env', 'get-values'], capture_output=True, text=True, cwd=cwd, check=False)
    if result.returncode:
        raise Exception("Failed to get azd environment values because of: " + result.stdout.strip())
    return result.stdout

def load_azd_env(
        cwd: Optional[StrOrBytesPath] = None,
        override: bool = False,
        ) -> bool:

    """Reads azd env variables and then load all the variables found as environment variables.

    Parameters:
        cwd: Current working directory to run the `azd env get-values` command.
        override: Whether to override the system environment variables with the variables
            from the `.env` file.
    Returns:
        Bool: True if at least one environment variable is set else False

    If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
    .env file.
    """

    from io import StringIO
    env_values = _azd_env_get_values(cwd)
    config = StringIO(env_values)
    return load_dotenv(
        stream=config,
        override=override,
        )
