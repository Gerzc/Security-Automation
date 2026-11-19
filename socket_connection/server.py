"""A basic TCP server for local client-server communication."""

import socket

# Listen only for connections from this Kali machine.
HOST = "127.0.0.1"
PORT = 5000


def main():
    """Create a TCP socket and listen for a client connection."""
    try:
        # Create an IPv4 TCP socket and close it automatically on exit.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Allow the listening address to be reused after restarting.
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Assign the local address and port to this socket.
            server_socket.bind((HOST, PORT))

            # Start listening for incoming connections.
            server_socket.listen(1)
            print(f"Server listening on {HOST}:{PORT}")
            print("Press Ctrl+C to stop the server.")

            # Wait for a client and create a socket for its connection.
            connection, address = server_socket.accept()
            with connection:
                print(f"Client connected from {address}")

                # Read incoming UTF-8 text one complete at a time.
                with connection.makefile(
                    "r", encoding="utf-8", errors="replace"
                ) as reader:
                    for line in reader:
                        message = line.rstrip("\n")
                        print(f"Client says: {message}")

                        # Acknowledge the client's request to disconnect.
                        if message.lower() == "quit":
                            connection.sendall(
                                "Goodbye!\n".encode("utf-8")
                            )
                            print("Client requested a clean disconnection.")
                            break

                        # Send a response ending with a newline.
                        response = f"Server received: {message}\n"
                        connection.sendall(response.encode("utf-8"))
                        print("Response sent to client.")


                print("Client connection closed.")

            print("Server shut down.")

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except OSError as error:
        print(f"Server error: {error}")



if __name__ == "__main__":
    main()