import pytest
from openapi_elm_client.generate import generate_elm_client
import tempfile
import subprocess
from pathlib import Path


@pytest.fixture(scope="module")
def elm_environment():
    with tempfile.TemporaryDirectory() as dirpath:
        subprocess.run(["elm", "init"], cwd=dirpath, input="y\n", text=True)
        for package in (
            "elm/http",
            "elm/url",
            "elm/json",
            "NoRedInk/elm-json-decode-pipeline",
            "elm-community/maybe-extra",
        ):
            subprocess.run(
                ["elm", "install", package], cwd=dirpath, input="y\n", text=True
            )
        yield Path(dirpath)


def test_compilation(elm_environment, corpus_spec):
    code = generate_elm_client(corpus_spec, "Test")
    (elm_environment / "src" / "Test.elm").write_text(code)
    proc = subprocess.run(["elm", "make", "src/Test.elm"], cwd=elm_environment)
    assert proc.returncode == 0
