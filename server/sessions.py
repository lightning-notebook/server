from pluto.identified import Identified, UUID
from pluto.notebook import Notebook
from typing import Dict, List, Optional


class ServerSession():
    """An abstract ServerSession which isn't necessarily part of a running Server."""
    notebooks: Dict[str, Notebook] = dict()

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
