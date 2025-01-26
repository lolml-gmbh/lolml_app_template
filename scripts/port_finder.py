import socket
from contextlib import closing


def is_port_available(port: int) -> bool:
    # First try to connect to the port
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            # Try connecting to the port
            result = sock.connect_ex(("127.0.0.1", port))
            if result == 0:  # Can connect = port is in use
                return False
        except OSError:
            pass  # Connection failed, which is what we want

    # Then try to bind to the port
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def find_next_free_port(start_port: int = 8000) -> int:
    port = start_port
    while not is_port_available(port):
        port += 1
    return port


if __name__ == "__main__":
    free_port = find_next_free_port(8501)
    print(free_port)
