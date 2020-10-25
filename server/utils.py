from pluto.notebook.file_format import from_file_format, to_file_format
from pluto.notebook import Notebook
from pathlib import Path
import os

NOTEBOOKS_FOLDER = "./samples"
NOTEBOOKS_FOLDER_PATH = Path(NOTEBOOKS_FOLDER).resolve()


def make_path(filename: str) -> Path:
    path = Path(os.path.join(NOTEBOOKS_FOLDER_PATH, filename)).resolve()

    if not path.is_relative_to(NOTEBOOKS_FOLDER_PATH):
        raise Exception

    return path


def load_notebook(filename: str) -> Notebook:
    try:
        path = make_path(filename)

        if not path.exists() or path.is_dir() or path.suffix != '.py':
            raise Exception

        with path.open('r') as file:
            data = file.read()
            notebook = from_file_format(data)
            return notebook

    except Exception as e:
        print("e", e)


def save_notebook(filename: str, notebook: Notebook):
    try:
        path = make_path(filename)

        if path.exists():
            if path.suffix == '.py':
                print("overwriting!")
            else:
                raise Exception

        with path.open('w') as file:
            data = to_file_format(notebook)
            file.write(data)

    except Exception as e:
        print("e", e)


if __name__ == "__main__":
    filename = './file_format.py'
    notebook = load_notebook(filename)
    notebook.cells[2].code = "b = 9956 # I changed you!"
    save_notebook(filename, notebook)
