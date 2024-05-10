from enum import IntEnum, auto
from json import dumps, loads


class MessageTypes(IntEnum):
    QUIT = auto()
    REPEAT = auto()
    MSG = auto()
    RUN_ENCRYPTED_CODE = auto()


class Message:
    def __init__(self, _type, data: dict = {}) -> None:
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Message):
            if self.type == other.type:
                if self.data == other.data:
                    return True
        return False


if __name__ == "__main__":
    orig = Message(MessageTypes.MSG, data={"g": "123"})
    encoded = orig.as_encoded()
    m = Message.from_encoded_str(encoded)
    assert orig == m
