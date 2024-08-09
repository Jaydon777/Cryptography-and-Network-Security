import socket
from threading import Thread

def encrypt(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def handle_client(client_socket, shift):
    with client_socket:
        while True:
            encrypted_message = client_socket.recv(1024).decode()
            if not encrypted_message:
                break
            print(f"Received encrypted message: {encrypted_message}")
            decrypted_message = decrypt(encrypted_message, shift)
            print(f"Decrypted message: {decrypted_message}")
            response = encrypt(decrypted_message, shift)
            client_socket.sendall(response.encode())
            print(f"Sent encrypted response: {response}")

def main():
    shift = 3  # Caesar cipher shift
    server_address = ('localhost', 65432)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen()
        print("Server is listening on port 65432 21BRS1419")
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to {client_address}")
            client_handler = Thread(target=handle_client, args=(client_socket, shift))
            client_handler.start()

if __name__ == "__main__":
    main()
