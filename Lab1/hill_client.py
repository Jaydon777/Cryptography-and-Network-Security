import socket

def get_key_matrix():
    print("Enter the key matrix dimensions (n x n):")
    n = int(input("Enter n (matrix size): "))
    print(f"Enter the {n}x{n} key matrix values:")
    key_matrix = []
    for i in range(n):
        row = list(map(int, input(f"Enter row {i+1}: ").strip().split()))
        key_matrix.extend(row)
    return key_matrix

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    key_matrix = get_key_matrix()
    key_matrix_str = ' '.join(map(str, key_matrix))
    client_socket.send(key_matrix_str.encode('utf-8'))
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
