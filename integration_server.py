import socket
import json
import psycopg2

# Konfigurasi Database (Sesuai Docker Compose)
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "mysecretpassword"

def create_table_if_not_exists():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patient_vitals (
                id SERIAL PRIMARY KEY,
                device_id VARCHAR(50),
                heart_rate INT,
                oxygen_level INT,
                status VARCHAR(20),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("[*] Memastikan tabel database tersedia... OK")
    except Exception as e:
        print(f"[!] Gagal membuat tabel: {e}")

def save_to_db(data):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        
        status = "NORMAL"
        if data['heart_rate'] > 120 or data['oxygen_level'] < 90:
            status = "CRITICAL ALERT"

        query = """
            INSERT INTO patient_vitals (device_id, heart_rate, oxygen_level, status)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (data['device_id'], data['heart_rate'], data['oxygen_level'], status))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"[INCOMING] Device: {data['device_id']} | BPM: {data['heart_rate']} | Status: {status} ✅")
        
    except Exception as e:
        print(f"[!] Database Error: {e}")

def start_server():
    create_table_if_not_exists()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print("[*] Integration Engine LISTENING on port 5000...")

    while True:
        client_socket, addr = server_socket.accept()
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                data = json.loads(message)
                save_to_db(data)
        except Exception as e:
            print(f"[!] Error processing data: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()