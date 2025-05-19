import socket
import time

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4000
    CHAR = 0x1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        
        prev_time = time.time()
        
        chars = []

        while True:
            data = s.recv(1)

            for byte in data:
                timestamp = time.time()
                relative_time = timestamp - prev_time
                prev_time = timestamp

                if relative_time < 0.6:
                    morse_char = "."
                elif relative_time < 1.5:
                    morse_char = "-"
                else:
                    morse_char = " "

                chars.append(morse_char)
                    
                print(f"Timer {relative_time:.2f} seconds, char: {morse_char}", flush=True)
                print(f"message: {''.join(chars)}")