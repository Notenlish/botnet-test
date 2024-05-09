import asyncio
import asyncudp


from message import Message, MessageTypes

from utils import get_config

IP, PORT = get_config()

global COUNT
global queue

COUNT = 0
QUEUE = []


async def message_creator():
    while True:
        if len(QUEUE) == 0:
            QUEUE.append(Message(MessageTypes.REPEAT, data={"count": COUNT}))
        # print("queue len is", len(QUEUE))
        await asyncio.sleep(0.1)


async def server(sock):
    while True:
        print("enters this loop")
        data, addr = await sock.recvfrom()
        msg_received = Message.from_encoded_str(data)

        print(msg_received)
        if msg_received.type == MessageTypes.REPEAT:
            COUNT = msg_received.data["count"]
            COUNT += 1

        if len(QUEUE) > 0:
            print("queue has an item")
            new_msg = QUEUE.pop(0)
            sock.sendto(new_msg.as_encoded(), addr)


# bütün problem bu create task şeyinden geliyo
# bunun nasıl olacağını düzgünce çizsem fln yeniden bi denesem sakin kafayla yaparım aga


async def main():
    sock = await asyncudp.create_socket(local_addr=(IP, PORT))

    task = asyncio.create_task(message_creator())
    await asyncio.gather(message_creator(), server(sock))

if __name__ == "__main__":
    asyncio.run(main())
