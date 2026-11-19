# Socket Connection Implementation

A basic TCP client-server application written in Python. The client sends messages, and the server acknowledges each message with a response.

## Environment

- Kali Linux
- Python 3
- Visual Studio Code
- Python standard library only; no additional packages required

## Files

- `server.py`: Listens for a client connection and responds to messages.
- `client.py`: Connects to the server and provides an interactive message prompt.
- `screenshots/`: Terminal screenshots documenting the required tests.

## Connection Settings

Both scripts use IPv4 TCP sockets with the following settings:

- Address: `127.0.0.1` (loopback)
- Port: `5000`
- Encoding: UTF-8
- Message boundary: newline (`\n`)

Both scripts run on the same machine. The server accepts one client connection per run and shuts down when that session ends.

## How to Run

Open two terminals in the `socket_connection` directory.

### 1. Start the server

```bash
python3 server.py
```

### 2. Start the client in the second terminal

```bash
python3 client.py
```

### 3. Exchange messages

At the client's `You:` prompt, enter a message and press Enter. The server displays the message and sends an acknowledgment, which the client displays.

### 4. Disconnect

Enter `quit` at the client's prompt. The server sends `Goodbye!`, and both scripts close their sockets and exit.

### 5. Test an unavailable server

With the server stopped, run the client again:

```bash
python3 client.py
```

The client displays:

```text
Connection refused. Make sure the server is running.
```

## Error Handling and Resource Cleanup

The scripts handle operating system and socket errors, as well as keyboard interruption. The client also handles connection refusal, connection timeout, and end-of-input.

Context managers (`with` statements) close sockets and socket readers when their blocks end, including during exception handling.

## Test Results

All required tests passed during manual testing.

| Test | Observed result | Evidence |
|---|---|---|
| Server listening | Server displayed its listening address and port. | [Screenshot 1](screenshots/01_server_listening.png) |
| Successful connection | Client and server displayed connection messages. | [Screenshot 2](screenshots/02_successful_connection.png) |
| Server receiving messages | Server displayed both test messages. | [Screenshot 3](screenshots/03_message_exchange.png) |
| Client receiving responses | Client displayed the server's acknowledgment for each message. | [Screenshot 3](screenshots/03_message_exchange.png) |
| Clean disconnection | Client received `Goodbye!`; both scripts exited without a traceback. | [Screenshot 4](screenshots/04_clean_disconnection.png) |
| Server not running | Client displayed a connection-refused message without a traceback. | [Screenshot 5](screenshots/05_server_not_running.png) |