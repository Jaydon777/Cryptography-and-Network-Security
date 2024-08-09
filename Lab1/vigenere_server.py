import socket

class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()
    
    def _format_text(self, text):
        return text.upper().replace(" ", "")
    
    def _generate_key(self, length):
        return (self.key * (length // len(self.key) + 1))[:length]
    
    def encrypt(self, plaintext):
        plaintext = self._format_text(plaintext)
        key = self._generate_key(len(plaintext))
        encrypted_text = []
        for p, k in zip(plaintext, key):
            encrypted_text.append(chr((ord(p) + ord(k) - 2 * ord('A')) % 26 + ord('A')))
        return ''.join(encrypted_text)
    
    def decrypt(self, ciphertext):
        ciphertext = self._format_text(ciphertext)
        key = self._generate_key(len(ciphertext))
        decrypted_text = []
        for c, k in zip(ciphertext, key):
            decrypted_text.append(chr((ord(c) - ord(k) + 26) % 26 + ord('A')))
        return ''.join(decrypted_text)

def handle_client(conn):
    try:
        key = conn.recv(1024).decode('utf-8').strip()
        cipher = VigenereCipher(key)

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
