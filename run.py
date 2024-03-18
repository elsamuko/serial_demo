#!/usr/bin/env python3

import serial
import subprocess as sp
import multiprocessing
import time

def server():
    tty2 = serial.Serial("tty2", timeout=2)
    if not tty2.is_open:
        tty2.open()
    res = tty2.read(17)
    print(res)
    tty2.close()


def client():
    tty1 = serial.Serial("tty1", timeout=2)
    if not tty1.is_open:
        tty1.open()
    tty1.write(b"Hello from client")
    tty1.close()


if __name__ == "__main__":
    print("Create socat virtual serial device")
    socat = sp.Popen(["socat", "pty,raw,echo=0,link=tty1", "pty,raw,echo=0,link=tty2"])
    time.sleep(1)

    print("Open tty2 and try reading")
    server_proc = multiprocessing.Process(target=server)
    server_proc.start()
    time.sleep(1)

    print("Open tty1 and try writing")
    client()

    print("Waiting for server")
    server_proc.join()
    socat.kill()
    socat.wait()
