#!/usr/bin/env python3

"""
Share a url on a local network
"""

import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_interface_ip(family: socket.AddressFamily) -> str:
    """
    Get the IP address of an external interface. Used when binding to
    0.0.0.0 or ::1 to show a more useful URL.

    Borrowed from werkzeug.serving.
    """

    # arbitrary private address
    host = "fd31:f903:5ab5:1::1" if family == socket.AF_INET6 else "10.253.155.219"

    with socket.socket(family, socket.SOCK_DGRAM) as s:
        try:
            s.connect((host, 58162))
        except OSError:
            return "::1" if family == socket.AF_INET6 else "127.0.0.1"

        return s.getsockname()[0]  # type: ignore


def main() -> None:
    """
    Entry point for share url. Asks for a url, generates the redirect,
    outputs the local share url, and hosts the server.
    """

    port = 8000

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(f'<script>window.location.href="{input("Enter a url: ")}";</script>')

    print(f"http://{get_interface_ip(socket.AF_INET)}:{port}")

    HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler).serve_forever()


if __name__ == "__main__":
    main()
