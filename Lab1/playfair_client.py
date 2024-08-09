import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    message = input("Enter message to encrypt with Playfair Cipher: ")
    keyword = input("Enter keyword for Playfair Cipher: ")
    client_socket.sendall(f"{message};{keyword}".encode('utf-8'))
    encrypted_message = client_socket.recv(1024).decode('utf-8')
    print(f"Received encrypted message: {encrypted_message}")
    client_socket.close()

if __name__ == "__main__":
    main()
