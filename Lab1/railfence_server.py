import socket

class RailFenceCipher:
    def __init__(self, num_rails):
        self.num_rails = num_rails
    
    def _create_rail_matrix(self, text):
        rail = [['\n' for _ in range(len(text))]
                for _ in range(self.num_rails)]
        direction = None
        row, col = 0, 0

        for char in text:
            if row == 0 or row == self.num_rails - 1:
                direction = not direction
            rail[row][col] = char
            col += 1
            row += 1 if direction else -1
        return rail

    def encrypt(self, text):
        rail = self._create_rail_matrix(text)
        ciphertext = ''.join([''.join(row).replace('\n', '') for row in rail])
        return ciphertext

    def decrypt(self, ciphertext):
        rail = [['\n' for _ in range(len(ciphertext))]
                for _ in range(self.num_rails)]
        index = 0
        for i in range(self.num_rails):
            row = 0
            for j in range(len(ciphertext)):
                if row == 0 or row == self.num_rails - 1:
                    if index < len(ciphertext):
                        rail[row][j] = ciphertext[index]
                        index += 1
                else:
                    if index < len(ciphertext):
                        rail[row][j] = ciphertext[index]
                        index += 1
                row = row + 1 if row < self.num_rails - 1 else row - 1

        result = []
        row, col = 0, 0
        for _ in ciphertext:
            if row == 0 or row == self.num_rails - 1:
                result.append(rail[row][col])
                col += 1
            row = row + 1 if row < self.num_rails - 1 else row - 1
        return ''.join(result)

def handle_client(conn):
    try:
        num_rails = int(conn.recv(1024).decode('utf-8').strip())
        cipher = RailFenceCipher(num_rails)

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
