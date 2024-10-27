from __future__ import annotations

from subprocess import CalledProcessError, run
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from os import PathLike


class AzdError(Exception):
    pass

class AzdCommandNotFoundError(AzdError):
    pass

class AzdEnvGetValuesError(AzdError):
    pass

class AzdNoProjectExistsError(AzdError):
    pass


def _azd_env_get_values(cwd: str | bytes | PathLike | None = None) -> str:
    try:
        result = run(
            ["/usr/bin/env", "azd", "env", "get-values"], capture_output=True, text=True, cwd=cwd, check=True
        )
    except CalledProcessError as e:
        if e.returncode == 127:
            raise AzdCommandNotFoundError("Cound not find command azd, install it prior to using dotenv-azd")
        if e.output.find("no project exists") > 0:
            raise AzdNoProjectExistsError
        raise AzdError("Unknown error occured")
    except Exception:
        raise AzdError("Unknown error occured")
    return result.stdout


def load_azd_env(
    cwd: str | bytes | PathLike | None = None,
    *,
    override: bool = False,
    ignore: bool = False
) -> bool:
    """Reads azd env variables and then load all the variables found as environment variables.

    Parameters:
        cwd: Current working directory to run the `azd env get-values` command.
        override: Whether to override the system environment variables with the variables
            from the `.env` file.
        ignore: Whether to ignore azd related errors and just silently load nothing
    Returns:
        Bool: True if at least one environment variable is set else False

    """

    from io import StringIO

    try:
        env_values = _azd_env_get_values(cwd)
    except AzdError as e:
        if ignore:
            return False
        else:
            raise e

    config = StringIO(env_values)
    return load_dotenv(
        stream=config,
        override=override,
    )
