# TCP Port Scanner

A Python TCP connect scanner that checks selected ports or an inclusive port range. It validates input, reports connection results, and displays timestamps and elapsed time.

## Environment and Dependencies

- Kali Linux
- Python 3
- Visual Studio Code
- Python standard library only
- Nmap for the separate external scanning demonstration

## Files

- `port_scanner.py`: Python scanner.
- `.gitignore`: Excludes generated Python cache files.
- `screenshots/`: Test evidence.
- `README.md`: Usage instructions and test documentation.

## Implementation

The program uses three functions:

- `parse_ports()`: Validates a comma-separated port list or one inclusive range. Ports must be between 1 and 65535. Duplicate ports are removed.
- `scan_port()`: Creates an IPv4 TCP socket, attempts a connection, and returns a status and explanation.
- `main()`: Collects input, checks the permitted target, resolves its IPv4 address, scans sequentially, and summarizes results.

Each connection attempt has a two-second timeout. A half-second delay separates attempts. Context managers close sockets automatically.

The input allowlist contains `127.0.0.1` and `scanme.nmap.org`. External selections are limited to 10 ports per run. Actual Python network scans documented here targeted localhost; the external demonstration used Nmap.

## Result Interpretation

| Status | Meaning |
|---|---|
| OPEN | A TCP connection succeeded. |
| CLOSED | The connection was explicitly refused. |
| TIMED OUT | The connection attempt exceeded the timeout. The port's state remains uncertain. |
| ERROR | Another operating system or socket error occurred; its explanation is displayed. |

An open port indicates a listening TCP service, not necessarily a vulnerability. A timeout does not establish that a port is closed or that the host is unreachable.

## Running the Python Scanner

From the `port_scanner` directory:

```bash
python3 port_scanner.py
```

Enter the target when prompted:

```text
127.0.0.1
```

Enter either selected ports:

```text
21,22,80,443
```

Or one inclusive range:

```text
7998-8002
```

Lists and ranges cannot be combined in a single input. Press Ctrl+C to interrupt the program.

## Test Activities and Evidence

### 1. Common Ports on Localhost

Scanned TCP ports 21, 22, 80, and 443 on `127.0.0.1`.

Observed result: all four ports were closed.

[Common-port scan screenshot](screenshots/01_localhost_common_ports.png)

### 2. Custom Range with Open and Closed Ports

Started a temporary HTTP server in a separate terminal:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Scanned `7998-8002` on `127.0.0.1`.

Observed result: port 8000 was open, and ports 7998, 7999, 8001, and 8002 were closed.

The HTTP server was stopped with Ctrl+C after testing.

[Custom-range screenshot](screenshots/02_localhost_custom_range.png)

### 3. Invalid Port Inputs

Tested the following inputs with target `127.0.0.1`:

| Input | Observed behavior |
|---|---|
| `0,70000` | Rejected ports outside the valid range. |
| `90-80` | Rejected a descending range. |
| `abc` | Reported an integer conversion error. |

Each run displayed an invalid-input message and exited without scanning or displaying a traceback.

[Invalid-input screenshot](screenshots/03_invalid_port_inputs.png)

### 4. Performance Comparison

Both tests targeted localhost with the temporary HTTP server stopped. All tested ports were closed.

| Port range | Port count | Elapsed time |
|---|---:|---:|
| `8000-8004` | 5 | 2.00 seconds |
| `8000-8019` | 20 | 9.52 seconds |

Elapsed time includes connection attempts, processing, and intentional delays. Five ports require four half-second delays; 20 ports require 19 delays. The measured durations closely matched those delay totals because localhost refused the connections quickly.

These measurements demonstrate total execution time under the configured pacing, rather than maximum scanning throughput.

[Five-port performance screenshot](screenshots/04_performance_5_ports.png)

[Twenty-port performance screenshot](screenshots/05_performance_20_ports.png)

### 5. Simulated Unreachable-Network Error

Used `unittest.mock.patch` to make socket creation raise:

```text
OSError(errno.ENETUNREACH, "Network is unreachable")
```

Called `scan_port("127.0.0.1", 80)` under that patch.

Observed result:

```text
Status: ERROR
Explanation: [Errno 101] Network is unreachable
PASS: unreachable-network error handled without a traceback.
```

No network traffic was sent during this test. It verifies the function's handling of a simulated operating system error; it is not a live unreachable-host test.

[Simulated error screenshot](screenshots/06_simulated_network_unreachable.png)

### 6. External Demonstration with Nmap

Used Nmap for a limited TCP connect scan of `scanme.nmap.org`, following Nmap's published scanning permission.

Commands:

```bash
date --iso-8601=seconds
nmap -sT -Pn -n -p 21,22,80,443 --scan-delay 500ms --max-retries 1 scanme.nmap.org
date --iso-8601=seconds
```

Observed results:

| TCP port | Nmap state |
|---|---|
| 21 | filtered |
| 22 | open |
| 80 | open |
| 443 | filtered |

Nmap reported a scan duration of 4.65 seconds. Filtered ports were not classified as closed.

This was a separate Nmap demonstration. The Python scanner was not executed against the external target.

[External Nmap screenshot](screenshots/07_scanme_selected_ports.png)

## Ethical Scope

Actual network scans were limited to localhost and `scanme.nmap.org`. Testing used sequential, paced connection attempts without exploitation or denial-of-service activity. Performance comparisons were conducted on localhost.

Nmap's published permission was consulted for the external demonstration:

https://nmap.org/book/legal-issues.html

## Test Coverage Notes

The Python scanner demonstrated common-port scanning, custom ranges, open and closed port detection, invalid-input handling, and performance across different ranges.

Unreachable-network handling was verified through simulation. External scanning was demonstrated with Nmap. These are documented separately from live tests of the Python scanner.