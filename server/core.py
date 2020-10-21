from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.dispatch import RPCDispatcher
from .sessions import ServerSession, ClientSession
import server.protocol as protocol
from typing import Set
import websockets as ws
import asyncio

rpc = JSONRPCProtocol()
dispatcher = RPCDispatcher()


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


class Server(ServerSession):
    server: ws.WebSocketServer
    clients: Set[Client] = set()

    def __init__(self) -> None:
        super().__init__()

    async def handler(self, socket: ws.WebSocketServerProtocol, url: str):
        client = Client(socket)
        self.clients.add(client)

        try:
            async for message in socket:
                print("message", message)
                response = protocol.handle_message(message)
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


server = Server()


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
