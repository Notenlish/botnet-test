from json import loads, dumps
from enum import IntEnum, auto


class MessageTypes(IntEnum):
    QUIT = auto()
    REPEAT = auto()
    MSG = auto()


class Message:
    def __init__(self, _type, data="") -> None:
        self.type = _type
        self.data = data

    def __str__(self) -> str:
        return f"< t: {MessageTypes(self.type).name},  d: {self.data} >"

    def as_dict(self) -> dict:
        return {"type": self.type, "data": self.data}

    def as_encoded(self) -> bytes:
        _str = dumps(self.as_dict())
        return _str.encode()

    @classmethod
    def from_dict(cls, _dict):
        return cls(_dict["type"], _dict["data"])

    @classmethod
    def from_str(cls, _str: str):
        _dict = loads(_str)
        # print(type(_dict), _dict)
        return cls.from_dict(_dict)

    @classmethod
    def from_encoded_str(cls, data: bytes):
        _str = data.decode()
        # print(_str, type(_str))
        return cls.from_str(_str)


if __name__ == "__main__":
    print(Message.from_encoded_str('{"type":3, "data":""}'.encode()))
