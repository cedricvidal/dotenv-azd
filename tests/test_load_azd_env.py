import subprocess
from pathlib import Path


class AzdEnvNewError(Exception):
    pass

def _azd_env_new(name: str, cwd: Path) -> str:
    result = subprocess.run(['azd', 'env', 'new', name], capture_output=True, text=True, cwd=cwd, check=False)
    if result.returncode:
        raise AzdEnvNewError("Failed to create azd env because of: " + result.stderr)
    return result.stdout


def test_load_azd_env(tmp_path: Path) -> None:
    from os import getenv

    from dotenv_azd import load_azd_env

    with open(tmp_path / "azure.yaml", "w") as config:
        config.write("name: dotenv-azd-test\n")

    _azd_env_new("test", tmp_path)
    var_set = load_azd_env(cwd=tmp_path)
    assert getenv('AZURE_ENV_NAME') is not None
    assert var_set
