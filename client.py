import asyncio

from message import Message, MessageTypes

from utils import get_config

IP, PORT = get_config()



async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(IP, PORT)

    while True:
        # if queue is empty, send messages every X seconds since its TCP protocol
        # TODO: 
        msg_to_send = Message(MessageTypes.MSG)
        print(f"Sending: {msg_to_send}")
        writer.write(msg_to_send.as_encoded())
        await writer.drain()

        data = await reader.read(100)
        msg_received = Message.from_encoded_str(data)
        print(f"Received: {msg_received}")

        if msg_received.type == MessageTypes.QUIT:
            break
        if msg_received.type == MessageTypes.REPEAT:
            pass

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()


asyncio.run(tcp_echo_client())
