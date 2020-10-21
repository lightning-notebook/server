from pluto.identified import Identified, UUID
from pluto.notebook import Notebook
from typing import Dict


class ServerSession():
    _notebooks: Dict[str, Notebook]

    @property
    def notebooks(self):
        return self._notebooks

    def __init__(self, notebooks: Dict[str, Notebook] = dict()) -> None:
        self._notebooks = notebooks

    def create_notebook(self, notebook_id: str):
        if notebook_id in self._notebooks:
            print("Notebook already exists")
            return

        self._notebooks[notebook_id] = Notebook(id=notebook_id)

    def add_notebook(self, notebook: Notebook):
        self._notebooks[notebook.id] = notebook

    def remove_notebook(self, notebook: Notebook):
        self._notebooks.pop(notebook.id)


class ClientSession(Identified):
    id: UUID
    notebook: Notebook

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
