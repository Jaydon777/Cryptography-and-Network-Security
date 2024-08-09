import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    key = input("Enter the key for Vigenère cipher: ")
    client_socket.send(key.encode('utf-8'))

    plaintext = input("Enter plaintext: ")
    client_socket.send(plaintext.encode('utf-8'))

    encrypted_text = client_socket.recv(1024).decode('utf-8')
    print(f"Received encrypted text: {encrypted_text}")

    client_socket.send(encrypted_text.encode('utf-8'))

    decrypted_text = client_socket.recv(1024).decode('utf-8')
    print(f"Received decrypted text: {decrypted_text}")

    client_socket.close()

if __name__ == "__main__":
    main()
