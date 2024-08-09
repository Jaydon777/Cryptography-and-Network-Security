import socket

class ColumnarTranspositionCipher:
    def __init__(self, key):
        self.key = key
        self.key_length = len(key)
    
    def _create_matrix(self, text):
        matrix = ['' for _ in range(self.key_length)]
        idx = 0
        for char in text:
            matrix[idx % self.key_length] += char
            idx += 1
        return matrix

    def _sort_key(self):
        return sorted(range(len(self.key)), key=lambda k: self.key[k])

    def encrypt(self, plaintext):
        plaintext = plaintext.replace(' ', '').upper()
        matrix = self._create_matrix(plaintext)
        sorted_key = self._sort_key()
        ciphertext = ''.join(''.join(matrix[i] for i in sorted_key))
        return ciphertext

    def decrypt(self, ciphertext):
        num_rows = len(ciphertext) // self.key_length
        sorted_key = self._sort_key()
        matrix = ['' for _ in range(self.key_length)]
        index = 0

        for i in sorted_key:
            matrix[i] = ciphertext[index:index + num_rows]
            index += num_rows

        plaintext = []
        for i in range(num_rows):
            for j in range(self.key_length):
                if i < len(matrix[j]):
                    plaintext.append(matrix[j][i])

        return ''.join(plaintext)

def handle_client(conn):
    try:
        key = conn.recv(1024).decode('utf-8').strip()
        cipher = ColumnarTranspositionCipher(key)

        plaintext = conn.recv(1024).decode('utf-8').strip()
        print(f"Received plaintext: {plaintext}")

        encrypted_text = cipher.encrypt(plaintext)
        print(f"Encrypted text: {encrypted_text}")

        conn.send(encrypted_text.encode('utf-8'))

        ciphertext = conn.recv(1024).decode('utf-8').strip()
        print(f"Received ciphertext: {ciphertext}")

        decrypted_text = cipher.decrypt(ciphertext)
        print(f"Decrypted text: {decrypted_text}")

        conn.send(decrypted_text.encode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen()

    print("Server is listening...")

    while True:
        conn, addr = server_socket.accept()
        print('Connected by 21BRS1419', addr)
        handle_client(conn)

if __name__ == "__main__":
    main()
