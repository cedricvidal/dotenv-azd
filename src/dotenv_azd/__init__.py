from __future__ import annotations

from subprocess import CalledProcessError, SubprocessError, run
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from os import PathLike


class AzdError(Exception):
    pass


class AzdCommandNotFoundError(AzdError):
    pass


class AzdNoProjectExistsError(AzdError):
    pass


E_CMD_NOT_FOUND = 127


def _azd_env_get_values(cwd: str | bytes | PathLike | None = None) -> str:
    try:
        result = run(["/usr/bin/env", "azd", "env", "get-values"], capture_output=True, text=True, cwd=cwd, check=True)
    except CalledProcessError as e:
        if e.returncode == E_CMD_NOT_FOUND or e.output.find("command not found") > 0:
            msg = "azd command not found, install it prior to using dotenv-azd"
            raise AzdCommandNotFoundError(msg) from e
        if e.output.find("no project exists") > 0:
            raise AzdNoProjectExistsError(e.output) from e
        msg = "Unknown error occured"
        raise AzdError(msg) from e
    except SubprocessError as e:
        msg = "Unknown error occured"
        raise AzdError(msg) from e
    return result.stdout


def load_azd_env(cwd: str | bytes | PathLike | None = None, *, override: bool = False, quiet: bool = False) -> bool:
    """Reads azd env variables and then load all the variables found as environment variables.

    Parameters:
        cwd: Current working directory to run the `azd env get-values` command.
        override: Whether to override the system environment variables with the variables
            from the `.env` file.
        quiet: Whether to suppress azd related errors.
    Returns:
        Bool: True if at least one environment variable is set else False

    """

    from io import StringIO

    try:
        env_values = _azd_env_get_values(cwd)
    except AzdError:
        if quiet:
            return False
        raise

    config = StringIO(env_values)
    return load_dotenv(
        stream=config,
        override=override,
    )
