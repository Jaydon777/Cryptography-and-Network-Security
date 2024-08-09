import socket

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

def main():
    shift = 3  # Caesar cipher shift
    server_address = ('localhost', 65432)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        while True:
            message = input("Enter message: ")
            encrypted_message = encrypt(message, shift)
            client_socket.sendall(encrypted_message.encode())
            print(f"Sent encrypted message: {encrypted_message}")
            response = client_socket.recv(1024).decode()
            print(f"Received encrypted response: {response}")
            decrypted_response = decrypt(response, shift)
            print(f"Decrypted response: {decrypted_response}")

if __name__ == "__main__":
    main()
