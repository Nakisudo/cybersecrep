
import socket
import time
import errno


class Scanner:
    """A simple TCP port scanner for authorized security testing."""

    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.closed_ports = []
        self.no_response_ports = []
        self.error_ports = []
        self.ip = None

    def resolve_target(self):
        """Resolve an IPv4 address or hostname."""
        try:
            self.ip = socket.gethostbyname(self.target)
            print(f"Target: {self.target} ({self.ip})")
            return True
        except socket.gaierror as error:
            print(f"Host resolution failed: {error}")
            return False

    def scan_port(self, port):
        """Attempt a TCP connection and classify the port status."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        try:
            result = sock.connect_ex((self.ip, port))

            if result == 0:
                return "OPEN"

            elif result == errno.ECONNREFUSED:
                return "CLOSED"

            elif result in (
                errno.ETIMEDOUT,
                errno.EHOSTUNREACH,
                errno.ENETUNREACH,
                errno.EHOSTDOWN
            ):
                return "NO RESPONSE"

            else:
                return "ERROR"

        except socket.timeout:
            return "NO RESPONSE"

        except OSError as error:
            print(f"Socket error on port {port}: {error}")
            return "ERROR"

        finally:
            sock.close()

    def scan(self, lower_port, upper_port):
        """Scan an inclusive range of TCP ports."""
        start_time = time.perf_counter()

        print(f"\nScanning ports {lower_port}-{upper_port}...")
        

        try:
            for port in range(lower_port, upper_port + 1):
                status = self.scan_port(port)

                if status == "OPEN":
                    self.open_ports.append(port)
                    print(f"Port {port}: OPEN")

                elif status == "CLOSED":
                    self.closed_ports.append(port)
                    print(f"Port {port}: CLOSED")

                elif status == "NO RESPONSE":
                    self.no_response_ports.append(port)
                    print(f"Port {port}: NO RESPONSE")

                else:
                    self.error_ports.append(port)
                    print(f"Port {port}: ERROR")

        except KeyboardInterrupt:
            print("\nScan interrupted by user.")

        elapsed = time.perf_counter() - start_time

        
        print("SCAN SUMMARY")
        print(f"Open ports: {len(self.open_ports)}")
        print(f"Closed ports: {len(self.closed_ports)}")
        print(f"No response: {len(self.no_response_ports)}")
        print(f"Errors: {len(self.error_ports)}")
        print(f"Time taken: {elapsed:.4f} seconds")

        return elapsed

    def write_results(self, filepath):
        """Save scan results to a text file."""
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(f"Target: {self.target}\n")
                file.write(f"Resolved IP: {self.ip}\n\n")

                file.write("OPEN PORTS\n")
                for port in self.open_ports:
                    file.write(f"{port}\n")

                file.write("\nCLOSED PORTS\n")
                for port in self.closed_ports:
                    file.write(f"{port}\n")

                file.write("\nNO RESPONSE\n")
                for port in self.no_response_ports:
                    file.write(f"{port}\n")

                file.write("\nERRORS\n")
                for port in self.error_ports:
                    file.write(f"{port}\n")

            print(f"Results saved to {filepath}")

        except OSError as error:
            print(f"Could not save results: {error}")


def main():
    print("PYTHON TCP PORT SCANNER")
    

    target = input("Enter target IP or hostname: ").strip()

    try:
        lower_port = int(input("Enter starting port: "))
        upper_port = int(input("Enter ending port: "))

        # Validate the port numbers
        if not (1 <= lower_port <= upper_port <= 65535):
            print("Invalid port range. Ports must be between 1 and 65535.")
            return

        scanner = Scanner(target)

        # Resolve the target before scanning
        if not scanner.resolve_target():
            return

        # Perform the scan and measure its duration
        scanner.scan(lower_port, upper_port)

        # Save results
        scanner.write_results("scan_results.txt")

    except ValueError:
        print("Invalid input. Enter whole numbers for the port range.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")


if __name__ == "__main__":
    main()
