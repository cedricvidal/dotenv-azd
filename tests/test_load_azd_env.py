import subprocess
from pathlib import Path

import pytest

from dotenv_azd import load_azd_env


class AzdEnvNewError(Exception):
    pass


class AzdEnvSetError(Exception):
    pass


def _azd_env_new(name: str, *, cwd: Path) -> str:
    result = subprocess.run(["azd", "env", "new", name], capture_output=True, text=True, cwd=cwd, check=False)
    if result.returncode:
        raise AzdEnvNewError("Failed to create azd env because of: " + result.stderr)
    return result.stdout


def _azd_env_set(key: str, value: str, *, cwd: Path) -> str:
    result = subprocess.run(["azd", "env", "set", key, value], capture_output=True, text=True, cwd=cwd, check=False)
    if result.returncode:
        raise AzdEnvSetError("Failed to set azd env value because of: " + result.stderr)
    return result.stdout


def test_load_azd_env(tmp_path: Path) -> None:
    from os import getenv

    with open(tmp_path / "azure.yaml", "w") as config:
        config.write("name: dotenv-azd-test\n")

    _azd_env_new("MY_AZD_ENV", cwd=tmp_path)
    var_set = load_azd_env(cwd=tmp_path)
    assert getenv("AZURE_ENV_NAME") == "MY_AZD_ENV"
    assert var_set


def test_load_azd_env_override(tmp_path: Path) -> None:
    from os import environ, getenv

    with open(tmp_path / "azure.yaml", "w") as config:
        config.write("name: dotenv-azd-test\n")

    environ["VAR1"] = "INITIAL"
    _azd_env_new("MY_AZD_ENV", cwd=tmp_path)
    _azd_env_set("VAR1", "OVERRIDE", cwd=tmp_path)
    var_set = load_azd_env(cwd=tmp_path)
    assert getenv("AZURE_ENV_NAME") == "MY_AZD_ENV"
    assert getenv("VAR1") == "INITIAL"
    assert var_set
    var_set = load_azd_env(cwd=tmp_path, override=True)
    assert getenv("VAR1") == "OVERRIDE"
    assert var_set


def test_load_azd_env_no_project_exists_error(tmp_path: Path) -> None:
    from dotenv_azd import AzdNoProjectExistsError

    with pytest.raises(AzdNoProjectExistsError, match="no project exists"):
        load_azd_env(cwd=tmp_path)


def test_load_azd_env_azd_command_not_found_error(tmp_path: Path) -> None:
    from os import environ

    from dotenv_azd import AzdCommandNotFoundError

    path = environ["PATH"]
    environ["PATH"] = ""
    with pytest.raises(AzdCommandNotFoundError):
        load_azd_env(cwd=tmp_path)
    environ["PATH"] = path


def test_load_azd_env_ignore_errors(tmp_path: Path) -> None:
    load_azd_env(cwd=tmp_path, quiet=True)
