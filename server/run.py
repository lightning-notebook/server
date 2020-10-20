from tinyrpc.protocols.jsonrpc import JSONRPCProtocol, JSONRPCRequest
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.exc import BadRequestError
from .sessions import ServerSession, ClientSession
from typing import Set
import websockets as ws
import asyncio

rpc = JSONRPCProtocol()
dispatcher = RPCDispatcher()


@dispatcher.public
def wow():
    return "hey!"


class Client(ClientSession):
    socket: ws.WebSocketServerProtocol

    def __init__(self, socket: ws.WebSocketServerProtocol) -> None:
        super(ClientSession, self).__init__()
        self.socket = socket

    async def notify(self, method, *args, **kwargs):
        try:
            message = rpc.create_request(
                method, args, kwargs, one_way=True).serialize()
            self.socket.send(message)
        except Exception as error:
            print("error", error)


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
        return request.error_respond(error)


class Server(ServerSession):
    port: int
    server: ws.WebSocketServer
    clients: Set[Client] = set()

    def __init__(self, port=1234) -> None:
        super(ServerSession, self).__init__()
        self.port = port

    async def handler(self, socket: ws.WebSocketServerProtocol, url: str):
        client = Client(socket)
        self.clients.add(client)

        try:
            async for message in socket:
                response = handle_message(message)
                print("response", response)
                if response != None:
                    await socket.send(response.serialize())
        finally:
            self.clients.remove(client)

    async def start(self):
        print(f"Running server on port: {self.port}")
        server = await ws.serve(self.handler, "localhost", self.port)
        self.server = server


async def run():
    server = Server()
    await server.start()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
    asyncio.get_event_loop().run_forever()
