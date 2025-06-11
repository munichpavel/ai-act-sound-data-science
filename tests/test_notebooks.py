'''
Test that demo notebook cells execute without errors
Using https://www.thedataincubator.com/blog/2016/06/09/testing-jupyter-notebooks/
'''
import os
from pathlib import Path
import subprocess
import tempfile

import pytest

import nbformat


project_root = Path(__file__).parent.parent
notebook_dir = project_root / 'notebooks'


@pytest.mark.parametrize(
    'notebook_path',
    [
        notebook_dir / 'eda-completed.ipynb',
        notebook_dir / 'extra-exercises.ipynb',
    ]
)
def test_ipynb(notebook_path, monkeypatch, tmpdir):

    # Set up mock output directories
    monkeypatch.setenv('SIMPSONS_DATA_DIR', str(tmpdir))
    monkeypatch.setenv('SIMPSONS_DOC_ROOT', str(tmpdir))

    errors = _notebook_run_errors(notebook_path)
    assert not errors


def _notebook_run_errors(path):
    """
    Execute a notebook via nbconvert and collect output.

    Idiosyncratic implementation partially due to windows NamedTemporaryFile +
    subprocess quirks. See

    https://stackoverflow.com/questions/46497842/passing-namedtemporaryfile-to-a-subprocess-on-windows

    and

    https://github.com/bravoserver/bravo/issues/111#issuecomment-826990
    """

    file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)

    args = [
        "python", "-m", "nbconvert", "--to", "notebook", "--execute",
        "--ExecutePreprocessor.timeout=60",
        "--output", file.name, path
    ]
    subprocess.check_call(args)

    file.seek(0)
    nb = nbformat.read(file, nbformat.current_nbformat)

    errors = [
        output for cell in nb.cells if "outputs" in cell
        for output in cell["outputs"] if output.output_type == "error"
    ]

    file.close()
    os.unlink(file.name)

    return errors