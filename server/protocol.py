from server.core import dispatcher, server
from pluto.cell import Cell
from typing import List


"""Requests: have a response"""


@dispatcher.public
def start_notebook(notebook_id: str) -> bool:
    try:
        if not notebook_id in server.notebooks:
            server.create_notebook(notebook_id)
        return True
    except:
        return False


@dispatcher.public
def stop_notebook(notebook_id: str) -> bool:
    try:
        if notebook_id in server.notebooks:
            server.stop_notebook(notebook_id)
        return True
    except:
        return False


@dispatcher.public
def get_cells(notebook_id: str) -> List[Cell]:
    notebook = server.notebooks[notebook_id]
    return notebook.cells


"""Notifications: have no response"""


@dispatcher.public
def add_cells(notebook_id: str, cells: List[Cell]) -> None:
    notebook = server.notebooks[notebook_id]
    for cell in cells:
        if cell.id in notebook.cells:
            print(f"Cell with id: {cell.id} already exists!")
            raise Exception
    notebook.run(cells=cells)


@dispatcher.public
def delete_cells(notebook_id: str, ids: List[str]) -> None:
    notebook = server.notebooks[notebook_id]
    notebook.cells = list(
        filter(lambda cell: cell.id not in ids, notebook.cells))
    notebook.run()


@dispatcher.public
def change_cells(notebook_id: str, cells: List[Cell]) -> None:
    notebook = server.notebooks[notebook_id]
    new_cells = {}
    for cell in cells:
        new_cells[cell] = cell.code
    notebook.run(cells=new_cells)
