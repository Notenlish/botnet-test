import asyncio
import asyncudp

from message import Message, MessageTypes

from utils import get_config

IP, PORT = get_config()

global COUNT
global queue

COUNT = 0
QUEUE = []


async def message_creator(flag):
    while True:
        if len(QUEUE) == 0:
            QUEUE.append(Message(MessageTypes.REPEAT, data={"count": COUNT}))
            flag.set()
        # print("queue len is", len(QUEUE))
        await asyncio.sleep(0.1)


async def client(sock, flag):
    while True:
        print("enters this loop")
        await flag.wait()
        if len(QUEUE) > 0:
            print("queue has an item")
            m_to_send = QUEUE.pop(0)
            sock.sendto(m_to_send.as_encoded())

        received, addr = await sock.recvfrom()
        msg_received = Message.from_encoded_str(received)
        print(msg_received)

        if msg_received.type == MessageTypes.QUIT:
            break
        if msg_received.type == MessageTypes.REPEAT:
            COUNT = msg_received.data["count"]
            COUNT += 1


async def main():
    sock = await asyncudp.create_socket(remote_addr=(IP, PORT))

    flag = asyncio.Event()

    task = asyncio.create_task(message_creator(flag))
    # await client(sock)

    await asyncio.gather(task, client(sock, flag))

    sock.close()


if __name__ == "__main__":
    asyncio.run(main())
