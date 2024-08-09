import socket

def preprocess_message(message):
    message = message.replace(" ", "").upper()
    message = message.replace("J", "I")
    digraphs = []
    i = 0
    while i < len(message):
        if i == len(message) - 1 or message[i] == message[i + 1]:
            digraphs.append(message[i] + 'X')
            i += 1
        else:
            digraphs.append(message[i] + message[i + 1])
            i += 2
    return digraphs

def create_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    key_set = set()
    matrix = []
    for char in key:
        if char not in key_set:
            key_set.add(char)
            matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in key_set:
            key_set.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return (i, j)
    return None

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    digraphs = preprocess_message(plaintext)
    ciphertext = []
    for digraph in digraphs:
        char1, char2 = digraph[0], digraph[1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        if row1 == row2:
            ciphertext.append(matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5])
        elif col1 == col2:
            ciphertext.append(matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2])
        else:
            ciphertext.append(matrix[row1][col2] + matrix[row2][col1])
    return "".join(ciphertext)

def handle_client_connection(conn, addr):
    print("Connected by", addr)
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        message, keyword = data.split(';')
        encrypted_message = playfair_encrypt(message, keyword)
        print(f"Received plaintext: {message}")
        print(f"Using keyword: {keyword}")
        print(f"Encrypted message: {encrypted_message}")
        conn.sendall(encrypted_message.encode('utf-8'))
    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server 21BRS1419 is listening on port 12345...")
    while True:
        conn, addr = server_socket.accept()
        handle_client_connection(conn, addr)

if __name__ == "__main__":
    main()
