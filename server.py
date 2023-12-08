import socket
import struct
import numpy as np
import random

def send_matrix(socket, matrix):
    matrix_bytes = matrix.tobytes()
    total_sent = 0
    while total_sent < len(matrix_bytes):
        sent = socket.send(matrix_bytes[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent
    print(f"Відправлено {total_sent} байтів.")

def receive_result_matrix(socket, shape):
    result_size_bytes = socket.recv(8)
    if not result_size_bytes:
        print("Не отримано розмір результату.")
        return None

    result_size = struct.unpack('!Q', result_size_bytes)[0]
    result_data = b''
    while len(result_data) < result_size:
        packet = socket.recv(result_size - len(result_data))
        if not packet:
            break
        result_data += packet

    return np.frombuffer(result_data, dtype=np.float64).reshape(shape)

def main():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))


        m, n, l = random.randint(1000, 10000), random.randint(1000, 10000), random.randint(1000, 10000)
        matrix_A = np.random.rand(m, n).astype(np.float64)
        matrix_B = np.random.rand(n, l).astype(np.float64)

        print(f"Розмір матриці A: {m}x{n}")
        print(f"Розмір матриці B: {n}x{l}")
        print("Сгенерована матриця A:")
        print(matrix_A)
        print("Сгенерована матриця B:")
        print(matrix_B)

        input("Натисніть Enter, щоб відправити матриці на сервер...")

        s.sendall(struct.pack('!QQQ', m, n, l))
        send_matrix(s, matrix_A)
        send_matrix(s, matrix_B)

        # Отримання та виведення результату
        result_matrix = receive_result_matrix(s, (m, l))
        print("Результат множення матриць:")
        print(result_matrix)

if __name__ == '__main__':
    main()
