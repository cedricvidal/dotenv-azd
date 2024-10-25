from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from os import PathLike


class AzdEnvGetValuesError(Exception):
    pass


def _azd_env_get_values(cwd: str | bytes | PathLike | None = None) -> str:
    result = subprocess.run(
        ["/usr/bin/env", "azd", "env", "get-values"], capture_output=True, text=True, cwd=cwd, check=False
    )
    if result.returncode:
        raise AzdEnvGetValuesError("Failed to get azd environment values because of: " + result.stdout.strip())
    return result.stdout


def load_azd_env(
    cwd: str | bytes | PathLike | None = None,
    *,
    override: bool = False,
) -> bool:
    """Reads azd env variables and then load all the variables found as environment variables.

    Parameters:
        cwd: Current working directory to run the `azd env get-values` command.
        override: Whether to override the system environment variables with the variables
            from the `.env` file.
    Returns:
        Bool: True if at least one environment variable is set else False

    """

    from io import StringIO

    env_values = _azd_env_get_values(cwd)
    config = StringIO(env_values)
    return load_dotenv(
        stream=config,
        override=override,
    )
