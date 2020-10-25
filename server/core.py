from pluto.notebook.notebook import Notebook
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol, JSONRPCRequest
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.exc import BadRequestError
from .sessions import ServerSession, ClientSession
from typing import Set, Dict
import websockets as ws
import asyncio

rpc = JSONRPCProtocol()
dispatcher = RPCDispatcher()


class Client(ClientSession):
    """Represents a currently connected Client which can be communicated with."""
    socket: ws.WebSocketServerProtocol

    def __init__(self, socket: ws.WebSocketServerProtocol) -> None:
        super(ClientSession, self).__init__()
        self.socket = socket

    async def sendNotification(self, method, *args, **kwargs):
        try:
            message = rpc.create_request(
                method, args, kwargs, one_way=True).serialize()
            self.socket.send(message)
        except Exception as error:
            print("error", error)

    async def sendRequest(self, method, *args, **kwargs):
        pass


class Server(ServerSession):
    """Represents a currently running Server which can receive/send messages."""
    server: ws.WebSocketServer
    clients: Set[Client] = set()

    def __init__(self) -> None:
        super(ServerSession, self).__init__()

    async def handler(self, socket: ws.WebSocketServerProtocol, url: str):
        client = Client(socket)
        self.clients.add(client)

        try:
            async for message in socket:
                print("message", message)
                response = handle_message(message)
                if response != None:
                    await socket.send(response.serialize())
        finally:
            self.clients.remove(client)

    async def start(self, port=1234):
        print(f"Running server on port: {port}")
        self.server = await ws.serve(self.handler, "localhost", port)

    async def stop(self):
        print("Stopping server...")
        self.server.close()
        await self.server.wait_closed()


"""
Single global instance of the Server: not sure if this is the best way to do this?
(this is imported in other files)
"""
server = Server()


def handle_message(message: ws.Data):
    """Either handles & responds with the valid request, or responds with an error."""
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
    """Either responds with the result of the method if it exists, or responds with an error."""
    try:
        method = dispatcher.get_method(request.method)
        result = method(*request.args, **request.kwargs)
        return request.respond(result)
    except Exception as error:
        print("error", error.with_traceback())
        return request.error_respond(error)


async def run():
    await server.start()


async def stop():
    await server.stop()


def main():
    try:
        asyncio.get_event_loop().run_until_complete(run())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
