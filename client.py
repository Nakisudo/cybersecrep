
import socket

# Server configuration
HOST = "127.0.0.1"
PORT = 5000


def start_client():
    # initialize the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Set a timeout to prevent indefinite connection attempts
        client_socket.settimeout(5)

        # Establish a connection with the server
        client_socket.connect((HOST, PORT))

        print(f"Successfully connected to server at {HOST}:{PORT}")
        print("Type a message and press Enter.")
        print("Type EXIT to disconnect.")

        # Continue sending messages until the client exits
        while True:
            message = input("Enter message: ")

            # Send the message to the server
            client_socket.sendall(message.encode("utf-8"))

            # Receive the server's response
            response = client_socket.recv(1024)

            if not response:
                print("Server disconnected.")
                break

            # display the server's response
            print("Server response:", response.decode("utf-8"))

            # stop communication when EXIT is entered
            if message.upper() == "EXIT":
                print("Disconnecting from server.")
                break

    except ConnectionRefusedError:
        print("Connection failed: The server not running.")

    except socket.timeout:
        print("Connection timed out.")

    except OSError as error:
        print(f"Client error: {error}")

    except KeyboardInterrupt:
        print("\nClient interrupted by user.")

    finally:
        # Close the client socket
        client_socket.close()
        print("Client socket closed.")


if __name__ == "__main__":
    start_client()
