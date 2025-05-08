import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from dotenv_azd import AzdCommandNotFoundError, AzdNoProjectExistsError, load_azd_env


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
    with open(tmp_path / "azure.yaml", "w") as config:
        config.write("name: dotenv-azd-test\n")

    _azd_env_new("MY_AZD_ENV", cwd=tmp_path)
    var_set = load_azd_env(cwd=tmp_path)
    assert os.getenv("AZURE_ENV_NAME") == "MY_AZD_ENV"
    assert var_set


def test_load_azd_env_override(tmp_path: Path, monkeypatch) -> None:
    with open(tmp_path / "azure.yaml", "w") as config:
        config.write("name: dotenv-azd-test\n")

    monkeypatch.setenv("VAR1", "INITIAL")
    _azd_env_new("MY_AZD_ENV", cwd=tmp_path)
    _azd_env_set("VAR1", "OVERRIDE", cwd=tmp_path)
    var_set = load_azd_env(cwd=tmp_path)
    assert os.getenv("AZURE_ENV_NAME") == "MY_AZD_ENV"
    assert os.getenv("VAR1") == "INITIAL"
    assert var_set
    var_set = load_azd_env(cwd=tmp_path, override=True)
    assert os.getenv("VAR1") == "OVERRIDE"
    assert var_set


def test_load_azd_env_no_project_exists_error(tmp_path: Path) -> None:
    with pytest.raises(AzdNoProjectExistsError, match="no project exists"):
        load_azd_env(cwd=tmp_path)


def test_load_azd_env_azd_command_not_found_error(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PATH", "")
    with pytest.raises(AzdCommandNotFoundError):
        load_azd_env(cwd=tmp_path)


def test_load_azd_env_ignore_errors(tmp_path: Path) -> None:
    load_azd_env(cwd=tmp_path, quiet=True)


@patch("dotenv_azd.run")
def test_cross_platform_direct_call_succeeds(mock_run):
    """Test that the function works when the direct call to azd succeeds."""
    # Mock subprocess.run to return success
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="DIRECT_TEST_VAR=direct_value", stderr=""
    )

    # This should complete without raising an exception
    result = load_azd_env(override=True)
    assert result is True
    assert os.environ.get("DIRECT_TEST_VAR") == "direct_value"
