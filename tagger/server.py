import socket
import struct

def prepare_data(data):
    header = struct.pack('>i', len(data))
    return header + data

def query_server(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9000))
    s.sendall(data)

    chunks = []
    while True:
        part = s.recv(0x1000)
        if len(part) <= 0:
            break

        chunks.append(part)

    s.close()

    return "".join(chunks)
