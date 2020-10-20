from pluto.identified import Identified, UUID
from pluto.notebook import Notebook
from typing import Dict


class ServerSession():
    notebooks: Dict[str, Notebook]

    def __init__(self, notebooks: Dict[str, Notebook] = dict()) -> None:
        self.notebooks = notebooks

    def add_notebook(self, notebook: Notebook):
        self.notebooks[notebook.id] = notebook

    def remove_notebook(self, notebook: Notebook):
        self.notebooks.pop(notebook.id)


class ClientSession(Identified):
    id: UUID
    notebook: Notebook

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
