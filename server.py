import asyncio
from utils import get_config
import time

from message import Message, MessageTypes

IP, PORT = get_config()


async def handle_echo(reader, writer):
    data = await reader.read(100)
    msg_received = Message.from_encoded_str(data)

    addr = writer.get_extra_info("peername")

    print(f"Received {msg_received} from {addr!r}")
    if msg_received.type == MessageTypes.REPEAT:
        pass

    msg_to_send = Message(MessageTypes.REPEAT, "asd")
    print(f"Sending: {msg_to_send}")
    writer.write(msg_to_send.as_encoded())
    await writer.drain()

    # print("Close the connection")
    # writer.close()
    # await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_echo, IP, PORT)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
