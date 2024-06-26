import asyncio
import asyncudp

from cryptography.fernet import Fernet

import json
from message import Message, MessageTypes

from utils import get_config

IP, PORT, KEY = get_config()

global COUNT
global queue

COUNT = 0
QUEUE = []


with open("script_to_send.txt", "r") as f:
    SCRIPT_TO_SEND = f.read()


async def server(sock):
    COUNT = 0

    encryptor = Fernet(KEY)

    while True:
        if len(QUEUE) == 0:
            QUEUE.append(Message(MessageTypes.REPEAT, data={"count": COUNT}))
        await asyncio.sleep(0.1)

        data, addr = await sock.recvfrom()
        msg_received = Message.from_encoded(data, encryptor)
        print(msg_received)

        if msg_received.type == MessageTypes.REPEAT:
            COUNT = msg_received.data["count"]
            COUNT += 1
            if COUNT % 10 == 0:
                data_to_send = {"script": SCRIPT_TO_SEND}
                QUEUE.append(
                    Message(
                        MessageTypes.RUN_ENCRYPTED_CODE,
                        data=data_to_send,
                    )
                )

        if len(QUEUE) > 0:
            new_msg = QUEUE.pop(0)
            sock.sendto(new_msg.as_encoded(encryptor), addr)


async def main():
    sock = await asyncudp.create_socket(local_addr=(IP, PORT))

    await server(sock)


if __name__ == "__main__":
    asyncio.run(main())
