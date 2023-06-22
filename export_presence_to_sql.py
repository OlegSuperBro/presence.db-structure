# shitty code but it works

import struct
import datetime
import sqlite3
from enum import IntFlag, Enum
from typing import List


def read_bool(buffer) -> bool:
    return struct.unpack("<?", buffer.read(1))[0]


def read_ubyte(buffer) -> int:
    return struct.unpack("<B", buffer.read(1))[0]


def read_ushort(buffer) -> int:
    return struct.unpack("<H", buffer.read(2))[0]


def read_uint(buffer) -> int:
    return struct.unpack("<I", buffer.read(4))[0]


def read_float(buffer) -> float:
    return struct.unpack("<f", buffer.read(4))[0]


def read_double(buffer) -> float:
    return struct.unpack("<d", buffer.read(8))[0]


def read_ulong(buffer) -> int:
    return struct.unpack("<Q", buffer.read(8))[0]


def read_string(buffer, encoding: str = "utf-8") -> str:
    strlen = 0
    strflag = read_ubyte(buffer)
    if (strflag == 0x0b):
        strlen = 0
        shift = 0
        # uleb128
        # https://en.wikipedia.org/wiki/LEB128
        while True:
            byte = read_ubyte(buffer)
            strlen |= ((byte & 0x7F) << shift)
            if (byte & (1 << 7)) == 0:
                break
            shift += 7
    return (struct.unpack("<" + str(strlen) + "s", buffer.read(strlen))[0]).decode(encoding)


def read_datetime(buffer) -> datetime.datetime:
    return datetime.datetime.min + datetime.timedelta(microseconds=read_ulong(buffer) / 10)


class Status(IntFlag):
    player = 1 << 0
    global_moderator = 1 << 1
    supporter = 1 << 2


class Gamemode(Enum):
    std = 0
    taiko = 2
    catch = 4
    mania = 6


def str_status(byte: str) -> List[bool]:
    try:
        tmp = repr(Status(int(byte[1], base=16)))
        tmp = tmp.split(".")[1]
        tmp = tmp.split(":")[0]
        tmp = tmp.split("|")
        return [True if "player" in tmp else False, True if "global_moderator" in tmp else False, True if "supporter" in tmp else False]
    except IndexError:
        return ["None", "None", "None"]


def str_gamemode(byte: str) -> str:
    try:
        tmp = repr(Gamemode(int(byte[0], base=16)))
        tmp = tmp.split(".")[1]
        tmp = tmp.split(":")[0]
        return tmp
    except IndexError:
        return "None"


if __name__ == "__main__":
    conn = sqlite3.connect("data.db")
    file = open("presence.db", "rb")

    read_uint(file)

    conn.execute("DROP TABLE users")
    conn.execute("""CREATE TABLE users (
                        id INTEGER,
                        username TEXT,
                        byte1 TEXT,
                        byte2 TEXT,
                        player INTEGER,
                        global_moderator INTEGER,
                        supporter INTEGER,
                        gamemode TEXT,
                        logitude REAL,
                        latitude REAL,
                        rank INTEGER,
                        timestamp DATE
                    );""")
    for _ in range(read_uint(file)):
        _id = read_uint(file)
        username = read_string(file)
        byte1 = hex(read_ubyte(file))[2:]
        byte2 = hex(read_ubyte(file))[2:]

        tmp1_byte = read_ubyte(file)
        tmp_byte = hex(tmp1_byte)[2:] if len(hex(tmp1_byte)[2:]) == 2 else "0" + hex(tmp1_byte)[2:]
        # print(tmp_byte)
        status = str_status(tmp_byte)
        player = status[0]
        global_moderator = status[1]
        supporter = status[2]
        gamemode = str_gamemode(tmp_byte)

        logitude = read_float(file)
        latitude = read_float(file)

        rank = read_uint(file)

        timestamp = read_datetime(file)

        conn.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (_id, username, byte1, byte2, player, global_moderator, supporter, gamemode,
                      logitude, latitude, rank, timestamp.strftime("%d/%m/%Y %H:%M:%S")))
    conn.commit()
    conn.close()
