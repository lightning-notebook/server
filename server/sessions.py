from pluto.identified import Identified, UUID
from pluto.notebook.file_format import from_file_format, to_file_format
from pluto.notebook import Notebook
from typing import Dict, Optional


class NotebookSession(Notebook):
    """A NotebookSession which is currently active & can be changed before saving to a file."""
    id: str
    path: str

    def __init__(self) -> None:
        super().__init__()

    def add_cell(self):
        pass

    def delete_cell(self):
        pass


def load_notebook(path: str) -> NotebookSession:
    pass


def save_notebook(path: str, notebook: NotebookSession):
    pass


NotebookSession.load_notebook = load_notebook
NotebookSession.save_notebook = save_notebook


class ServerSession():
    """An abstract ServerSession which isn't necessarily part of a running Server."""
    notebook_sessions: Dict[str, NotebookSession] = dict()

    def __init__(self) -> None:
        pass

    def create_notebook(self, notebook_id: str):
        if notebook_id in self.notebooks:
            print("Notebook already exists")
            return

        self.notebooks[notebook_id] = Notebook(id=notebook_id)

    def start_notebook(self, notebook_id: str):
        self.create_notebook(notebook_id=notebook_id)

    def stop_notebook(self, notebook_id: str):
        self.notebooks.pop(notebook_id)


class ClientSession(Identified):
    """An abstract ClientSession which isn't necessarily associated with a connected Client."""
    id: str
    notebook_id: str

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
