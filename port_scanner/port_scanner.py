"""A TCP port scanner for the targets permitted by the assignment."""

import socket
import time
from datetime import datetime

# Restrict scanning to the targets permitted by the assignment.
ALLOWED_TARGETS = ("127.0.0.1", "scanme.nmap.org")

# Maximum time in seconds to wait for each connection attempt.
CONNECTION_TIMEOUT = 2.0

# Pause between connection attempts to keep scanning sequential and paced.
SCAN_DELAY = 0.5


def parse_ports(port_input):
    """Convert a comma-separated list or inclusive range into valid ports."""
    port_input = port_input.strip()

    if not port_input:
        raise ValueError("Enter at least one port.")

    if "-" in port_input:
        # Accept one range, such as 20-25.
        if "," in port_input or port_input.count("-") != 1:
            raise ValueError("Use a port list or one range, such as 20-25.")

        start_text, end_text = port_input.split("-")
        start = int(start_text)
        end = int(end_text)

        if not 1 <= start <= end <= 65535:
            raise ValueError(
                "Range must be ascending and between 1 and 65535."
            )

        ports = list(range(start, end + 1))
    else:
        # Accept individual ports separated by commas.
        ports = [int(value.strip()) for value in port_input.split(",")]

        if any(port < 1 or port > 65535 for port in ports):
            raise ValueError("Port numbers must be between 1 and 65535.")

    # Remove duplicate ports and return them in ascending order.
    return sorted(set(ports))


def scan_port(target_ip, port):
    """Attempt a TCP connection and return its status and explanation."""
    try:
        # Create a new socket for this port and close it after the attempt.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scan_socket:
            scan_socket.settimeout(CONNECTION_TIMEOUT)
            scan_socket.connect((target_ip, port))
            return "OPEN", "TCP connection succeeded."

    except ConnectionRefusedError:
        return "CLOSED", "Connection refused."

    except TimeoutError:
        return "TIMED OUT", "No response before the connection timeout."

    except OSError as error:
        return "ERROR", str(error)


def main():
    """Validate input, scan permitted targets, and summarize results."""
    print(f"Session started: {datetime.now().astimezone().isoformat(timespec='seconds')}")

    try:
        target = input("Target (127.0.0.1 or scanme.nmap.org): ").strip().lower()

        if target not in ALLOWED_TARGETS:
            raise ValueError(
                "Target must be 127.0.0.1 or scanme.nmap.org."
            )

        port_input = input("Ports (example: 22,80,443 or 20-25): ")
        ports = parse_ports(port_input)

        # Keep each external scan small.
        if target == "scanme.nmap.org" and len(ports) > 10:
            raise ValueError("Select at most 10 ports for scanme.nmap.org.")

        # Resolve the target once, then use that IPv4 address.
        target_ip = socket.gethostbyname(target)

        print(f"\nTarget: {target} ({target_ip})")
        print(f"Ports selected: {len(ports)}")
        print(f"Timeout: {CONNECTION_TIMEOUT}s; delay: {SCAN_DELAY}s")
        print(f"Scan started: {datetime.now().astimezone().isoformat(timespec='seconds')}\n")

        counts = {"OPEN": 0, "CLOSED": 0, "TIMED OUT": 0, "ERROR": 0}
        started = time.perf_counter()

        for index, port in enumerate(ports):
            # Pause between attempts, but not before the first attempt.
            if index > 0:
                time.sleep(SCAN_DELAY)

            status, explanation = scan_port(target_ip, port)
            counts[status] += 1
            print(f"Port {port:5d}/tcp  {status:10s}  {explanation}")

        elapsed = time.perf_counter() - started

        print("\nScan complete.")
        print(f"Scan ended: {datetime.now().astimezone().isoformat(timespec='seconds')}")
        print(f"Elapsed time: {elapsed:.2f} seconds")

        for status, count in counts.items():
            print(f"{status}: {count}")

    except ValueError as error:
        print(f"Invalid input: {error}")
    except socket.gaierror as error:
        print(f"Hostname resolution failed: {error}")
    except OSError as error:
        print(f"Network/system error: {error}")
    except EOFError:
        print("\nInput ended. Scanner stopped.")
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")


if __name__ == "__main__":
    main()