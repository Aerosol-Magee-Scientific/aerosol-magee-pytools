# Copyright (c) 2026 Aerosol d.o.o.
# Licensed under the Aerosol Magee Scientific Software License (see LICENSE file for details)

import re
import socket

# default parameters:
INSTRUMENT_PORT = 8002  # always the same
BUFFER_SIZE = 4096  # always the same
RECV_TIMEOUT = 2.0  # seconds


def receive_all(sock, buffer_size=BUFFER_SIZE, timeout=RECV_TIMEOUT):
    sock.settimeout(timeout)
    chunks = []
    while True:
        try:
            chunk = sock.recv(buffer_size)
            if not chunk:
                break
            chunks.append(chunk)
        except socket.timeout:
            break

    received = b''.join(chunks)
    received_text = received.decode(errors='replace').rstrip('\r\n\x00\x03')
    return received_text

def request_tcp(ip, command, port=INSTRUMENT_PORT, buffer_size=BUFFER_SIZE, timeout=RECV_TIMEOUT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            s.send(command.encode())
            return receive_all(s, buffer_size=buffer_size, timeout=timeout)
    except socket.timeout:
        return None

def guess_delimiter(sample_text):
    candidates = [',', '\t', '|', ';']
    counts = {sep: sample_text.count(sep) for sep in candidates}
    best = max(counts, key=counts.get)
    if counts[best] > 0:
        return best
    if re.search(r'\s{2,}', sample_text):
        return r'\s+'
    return ','