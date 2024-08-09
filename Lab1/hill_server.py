import socket
import numpy as np

class HillCipher:
    def __init__(self, key_matrix):
        self.key_matrix = np.array(key_matrix)
        self.inv_key_matrix = self._invert_matrix(self.key_matrix)

    def _mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def _invert_matrix(self, matrix):
        det = int(round(np.linalg.det(matrix))) % 26
        det_inv = self._mod_inverse(det, 26)
        matrix_mod = np.mod(matrix, 26)
        matrix_inv = det_inv * np.round(det * np.linalg.inv(matrix_mod)).astype(int) % 26
        return matrix_inv

    def encrypt(self, plaintext):
        plaintext = plaintext.upper().replace(" ", "")
        n = self.key_matrix.shape[0]
        plaintext = [ord(c) - ord('A') for c in plaintext]
        plaintext += [0] * ((n - len(plaintext) % n) % n)
        plaintext_matrix = np.array(plaintext).reshape(-1, n)
        encrypted_matrix = (plaintext_matrix @ self.key_matrix) % 26
        encrypted_text = ''.join(chr(num + ord('A')) for num in encrypted_matrix.flatten())
        return encrypted_text

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.upper().replace(" ", "")
        n = self.inv_key_matrix.shape[0]
        ciphertext = [ord(c) - ord('A') for c in ciphertext]
        ciphertext_matrix = np.array(ciphertext).reshape(-1, n)
        decrypted_matrix = (ciphertext_matrix @ self.inv_key_matrix) % 26
        decrypted_text = ''.join(chr(num + ord('A')) for num in decrypted_matrix.flatten())
        return decrypted_text.strip()

def handle_client(conn):
    try:
        key_matrix_str = conn.recv(1024).decode('utf-8').strip()
        key_matrix = [list(map(int, key_matrix_str.split()[i:i+3])) for i in range(0, len(key_matrix_str.split()), 3)]
        cipher = HillCipher(key_matrix)
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
