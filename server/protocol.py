from tinyrpc.protocols.jsonrpc import JSONRPCRequest
from tinyrpc.exc import BadRequestError
from pluto.cell import Cell
from typing import List
import websockets as ws
from server.core import dispatcher, server, rpc


@dispatcher.public
def start_notebook(notebook_id: str):
    if not notebook_id in server.notebooks:
        server.create_notebook(notebook_id)

    notebook = server.notebooks[notebook_id]
    return notebook.cells


@dispatcher.public
def add_cells(notebook_id: str, cells: List[Cell]):
    notebook = server.notebooks[notebook_id]
    for cell in cells:
        if cell.id in notebook.cells:
            print(f"Cell with id: {cell.id} already exists!")
            raise Exception


@dispatcher.public
def change_cells(notebook_id: str, cells: List[Cell]):
    notebook = server.notebooks[notebook_id]


def handle_message(message: ws.Data):
    try:
        request = rpc.parse_request(message)
    except BadRequestError as error:
        response = error.error_respond(error)
    else:
        if hasattr(request, "create_batch_response"):
            response = request.create_batch_response(
                handle_request(req) for req in request
            )
        else:
            response = handle_request(request)

    return response


def handle_request(request: JSONRPCRequest):
    try:
        method = dispatcher.get_method(request.method)
        result = method(*request.args, **request.kwargs)
        return request.respond(result)
    except Exception as error:
        print("error", error.with_traceback())
        return request.error_respond(error)
