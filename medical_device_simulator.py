import socket
import json
import time
import random

def simulate_device():
    host = 'localhost'
    port = 5000 

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            data = {
                "device_id": "ICU-MONITOR-01",
                "heart_rate": random.randint(60, 140), 
                "oxygen_level": random.randint(85, 100),
                "timestamp": time.time()
            }

            message = json.dumps(data)
            client_socket.send(message.encode('utf-8'))
            print(f"[>] Terkirim: BPM {data['heart_rate']}, SpO2 {data['oxygen_level']}")
            client_socket.close()
            
        except ConnectionRefusedError:
            print("[!] Server belum nyala. Mencoba lagi...")
        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(1)

if __name__ == "__main__":
    simulate_device()