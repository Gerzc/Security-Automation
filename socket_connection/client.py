"""A basic TCP client for local client-server communication."""

import socket

# Connect to the server running on this Kali machine.
HOST = "127.0.0.1"
PORT = 5000


def main():
    """Connect to the TCP server."""
    try:
        # Create an IPv4 TCP socket and close it automatically on exit.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Limit how long the initial connection attempt can take.
            client_socket.settimeout(5)
            client_socket.connect((HOST, PORT))

            # Return to blocking mode for the interactive conversation.
            client_socket.settimeout(None)
            print(f"Connected to server at {HOST}:{PORT}")
            print("Type a message, or type 'quit' to disconnect.")

            # Read server responses one complete line at a time.
            with client_socket.makefile(
                "r", encoding="utf-8", errors="replace"
            ) as reader:
                while True:
                    message = input("You: ")

                    # End each message with a newline before sending.
                    client_socket.sendall(
                        (message + "\n").encode("utf-8")
                    )

                    # Wait for the server's response.
                    response = reader.readline()

                    # An empty string means the server closed the connection.
                    if not response:
                        print("Server closed the connection.")
                        break

                    print(response.rstrip("\n"))

                    # Exit after receiving the server's goodbye response.
                    if message.lower() == "quit":
                        print("Clean disconnection completed.")
                        break


            print("Closing client connection.")

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    except TimeoutError:
        print("Connection timed out.")
    except OSError as error:
        print(f"Client error: {error}")
    except KeyboardInterrupt:
        print("\nClient stopped by user.")
    except E0FError:
        print("\nInput ended. Closing client connection.")


if __name__ == "__main__":
    main()