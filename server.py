
import socket

# Server configuration
HOST = "127.0.0.1"  # Localhost IP address
PORT = 5000         # Port on which the server listens


def start_server():
    # Initializing the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow the address to be reused after the server shuts down
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind the socket to the specified IP address and port
        server_socket.bind((HOST, PORT))

        # Start listening for incoming connections
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for a client connection...")

        # Accept an incoming client connection
        client_socket, client_address = server_socket.accept()

        print(f"Connected to client: {client_address}")

        # Handle communication with the connected client
        with client_socket:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)

                # Check whether the client has disconnected
                if not data:
                    print("Client disconnected.")
                    break

                # Convert received bytes into a string
                message = data.decode("utf-8")

                print(f"Client says: {message}")

                # Check whether the client wants to disconnect
                if message.upper() == "EXIT":
                    response = "Goodbye! Connection closing."
                    client_socket.sendall(response.encode("utf-8"))
                    print("Client requested disconnection.")
                    break

                # Process the message and prepare a response
                response = f"Server received your message: {message}"

                # Send the response back to the client
                client_socket.sendall(response.encode("utf-8"))

                print(f"Response sent: {response}")

    except OSError as error:
        print(f"Server error: {error}")

    except KeyboardInterrupt:
        print("\nServer interrupted by user.")

    finally:
        # Close the server socket
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    start_server()
