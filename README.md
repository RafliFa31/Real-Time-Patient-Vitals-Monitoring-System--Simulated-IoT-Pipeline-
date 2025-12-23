# 🏥 VitalFlow: Real-Time Patient Vitals Integration Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Protocol](https://img.shields.io/badge/Protocol-TCP%2FIP-red?style=for-the-badge)

## 📄 Overview
Proyek ini mengimplementasikan pipeline integrasi data end-to-end untuk memonitor tanda-tanda vital pasien (Detak Jantung & SpO2) secara real-time. Dimulai dengan simulator alat medis sebagai fondasi, arsitektur ini dirancang untuk menjembatani kesenjangan antara perangkat keras medis yang mengirimkan data mentah (raw stream) dengan sistem database modern. Tujuan utamanya adalah mensimulasikan lingkungan ICU digital di mana data pasien diproses, divalidasi, dan divisualisasikan detik demi detik untuk mendukung pengambilan keputusan medis yang cepat.

Pipeline ini diorkestrasi menggunakan Docker Compose, dengan Python sebagai inti logika untuk Socket Programming (TCP/IP). Data ditangkap dan diproses oleh Integration Server, disimpan ke dalam PostgreSQL yang berjalan di dalam container, dan divisualisasikan melalui dashboard Streamlit interaktif. Platform ini juga dilengkapi dengan Anomaly Detection System otomatis yang langsung menandai status "CRITICAL" jika tanda vital pasien melebihi ambang batas aman.

---

## 🎯 Objectives
- 📡 **Simulasi Streaming:** Mensimulasikan aliran data dari perangkat medis menggunakan protokol TCP/IP.
- 🔄 **Data Parsing:** Menerjemahkan data mentah format JSON/Bytes menjadi data terstruktur SQL.
- 🛡️ **Automated Validation:** Melakukan validasi otomatis untuk mendeteksi anomali kesehatan (contoh: BPM > 120).
- 📊 **Real-Time Visualization:** Memvisualisasikan tren kesehatan pasien secara *live* via dashboard interaktif.
- 🐳 **Infrastructure:** Membangun infrastruktur database yang terisolasi dan konsisten menggunakan Docker.

---

## 📁 Project Structure
```bash
vitalflow_iot_pipeline/
├── images/
│   └── screenshot.png          # Bukti tampilan dashboard
├── dashboard.py                # Visualisasi Frontend (Streamlit)
├── docker-compose.yml          # Orkestrasi Database PostgreSQL
├── integration_server.py       # Backend: TCP Listener & Logic Penyimpanan
├── medical_device_simulator.py # Frontend: Simulator Pengirim Data
├── README.md                   # Dokumentasi Proyek
└── requirements.txt            # Daftar Pustaka Python
```

## 📚 Data Sources

Sistem ini dirancang dengan fleksibilitas tinggi. Saat ini menggunakan data sintetik untuk simulasi, namun arsitekturnya siap untuk integrasi perangkat keras nyata.

| Status | Sumber Data | Deskripsi Teknis |
| :--- | :--- | :--- |
| **🟢 Current** | **Synthetic Generator** | Menggunakan modul `random` Python untuk mensimulasikan variabilitas detak jantung (60-140 BPM) dan saturasi oksigen (85-100%) secara statistik. |
| **🟡 Future** | **HL7 / FHIR** | Integrasi standar interoperabilitas data kesehatan internasional untuk pertukaran data antar sistem rumah sakit. |
| **🟡 Future** | **Serial Port (USB)** | Pembacaan data fisik dari mikrokontroler seperti Arduino atau Raspberry Pi via kabel serial. |
| **🟡 Future** | **Wearable Webhooks** | Endpoint HTTP untuk menerima *push data* dari smartwatch atau API kesehatan pihak ketiga. |

## ✨ Features

| Fitur | Deskripsi |
| :--- | :--- |
| 🌐 **Real-Time Ingestion** | Menangkap data streaming via TCP Socket tanpa latensi signifikan. |
| 🧠 **Automated Parsing** | Mengubah data *unstructured* menjadi *structured* secara otomatis. |
| 🛡️ **Anomaly Detection** | Logika backend yang langsung memfilter kondisi kritis sebelum data disimpan. |
| 🗄️ **Containerized Storage** | Database PostgreSQL yang berjalan dalam container Docker untuk isolasi lingkungan. |
| 📊 **Live Dashboard** | Visualisasi grafik garis yang bergerak otomatis (*auto-refresh*) setiap detik. |
| 🔁 **Scalable Architecture** | Desain modular yang memisahkan *Sender*, *Receiver*, dan *Storage*. |

## 🛠️ Tech Stack
| Component | Tool |
| :--- | :--- |
| **Communication Protocol** | TCP/IP Sockets (Layer 4) |
| **Backend Logic** | Python (Socket, JSON, Psycopg2) |
| **Data Storage** | PostgreSQL 13 |
| **Infrastructure** | Docker & Docker Compose |
| **Visualization** | Streamlit & Pandas |
| **Data Simulation** | Python Random Module |

## 🔄 Pipeline Overview

Sistem ini menggunakan arsitektur linear data pipeline. Berikut adalah alur data dari hulu ke hilir beserta teknologi yang digunakan:

```text
STEP 1: DATA GENERATION 🩺
[ Medical Device Simulator ]
   🛠️ Tools: Python (Random Lib)
   📄 Data: Raw JSON (Heart Rate, SpO2)
            ⬇
            ⬇  (Transmission via TCP/IP Socket)
            ⬇
STEP 2: INGESTION & LOGIC 🧠
[ Integration Server ]
   🛠️ Tools: Python (Socket, Json), Docker
   ⚙️ Process: 
       1. Receive Bytes
       2. Parse to JSON
       3. Anomaly Check (if BPM > 120 -> Critical)
            ⬇
            ⬇  (SQL Insert)
            ⬇
STEP 3: STORAGE 🗄️
[ Persistent Database ]
   🛠️ Tools: PostgreSQL 13, Docker Container
   ⚙️ Process: Storing structured historical data
            ⬇
            ⬇  (SQL Query / Pandas Read)
            ⬇
STEP 4: VISUALIZATION 📊
[ Monitoring Dashboard ]
   🛠️ Tools: Streamlit, Pandas
   ⚙️ Process: Real-time fetching & Graph plotting
```

### ⚙️ Workflow Mechanics

#### 📡 Step 1: Data Generation (The Source)
* **Component:** `medical_device_simulator.py`
* **Action:** Script ini bertindak sebagai alat medis virtual.
* **Logic:** Membangkitkan data dummy (*Heart Rate* 60-140 bpm & *SpO2* 80-100%) secara acak.
* **Output:** Mengirimkan paket data JSON ke `localhost:5000` via **TCP Socket**.

#### 🧠 Step 2: Ingestion & Processing (The Brain)
* **Component:** `integration_server.py`
* **Action:** Server mendengarkan (*listen*) koneksi masuk pada port `5000`.
* **Logic:** 1. Menerima raw bytes dan melakukan decoding ke JSON.
    2. **Validasi:** Jika `BPM > 120` atau `SpO2 < 90`, status diset **CRITICAL**.
    3. **Load:** Menyimpan data bersih ke tabel `patient_vitals` di PostgreSQL.

#### 📊 Step 3: Monitoring (The View)
* **Component:** `dashboard.py` (Streamlit)
* **Action:** Melakukan *polling* ke database setiap 1 detik.
* **Logic:**
    * `SELECT * FROM patient_vitals ORDER BY time DESC LIMIT 1` untuk angka real-time.
    * Menampilkan grafik garis (*Line Chart*) untuk melihat tren historis.


## 🚀 Quick Start

### 📋 Prerequisites
Ensure you have the following installed and running on your machine:
* **Docker Desktop** (Must be running status)
* **Python 3.8+**
* **Git**

### 🛠️ Installation & Setup

**1. Clone the Repository**
Open your terminal and clone the project:
```bash
git clone https://github.com/RafliFa31/vitalflow_iot_pipeline.git
cd vitalflow_iot_pipeline
```

**2. Setup Infrastructure Start the PostgreSQL database container using Docker Compose**
```bash
docker-compose up -d
```
(Wait until the container is fully healthy)

🖥️ Run the Application
You need to open 3 separate terminals to simulate the full ecosystem:

Terminal 1: Start the Integration Server This acts as the backend listener.
```bash
python integration_server.py
```
Terminal 2: Start the Medical Simulator This generates and sends dummy vital sign data.
```bash
python medical_device_simulator.py
```
Terminal 3: Launch the Dashboard This runs the frontend visualization.
```bash
streamlit run dashboard.py
```
🌐 Access the Dashboard
Once running, open your browser and go to: http://localhost:8501

---

## ⚠️ Current Limitations
> **Note:** Proyek ini adalah simulasi perangkat lunak untuk tujuan edukasi dan belum siap untuk penggunaan medis klinis nyata.

* **🚧 Simulasi Lokal:** Komunikasi data saat ini hanya berjalan di *localhost* atau jaringan lokal (LAN), belum terhubung ke Cloud publik.
* **🔌 Direct Socket:** Belum menggunakan *Message Broker* (seperti Kafka/RabbitMQ), sehingga risiko *packet loss* masih ada jika server down mendadak.
* **🔓 Keamanan:** Data dikirim dalam format JSON biasa (*plain text*) dan belum dienkripsi dengan SSL/TLS.
* **💻 Single Device:** Dioptimalkan untuk mensimulasikan satu alat monitor; belum mendukung ribuan koneksi konkuren (*concurrency*).

## 🔮 Future Development Plans
Berikut adalah roadmap pengembangan untuk fase berikutnya:

- [ ] **Message Broker Integration:** Mengimplementasikan Apache Kafka/RabbitMQ untuk antrian data bervolume tinggi.
- [ ] **HL7 Standard:** Mengadopsi standar format data kesehatan internasional (HL7/FHIR).
- [ ] **Security Hardening:** Menambahkan enkripsi SSL/TLS pada komunikasi socket.
- [ ] **Cloud Deployment:** Deploy sistem ke AWS (EC2) atau Google Cloud Platform.
- [ ] **AsyncIO Support:** Mengembangkan server *asynchronous* untuk menangani ribuan koneksi sekaligus.

---

## ⚠️ Current Limitations
Saat ini, sistem memiliki beberapa batasan karena fokus utamanya adalah simulasi konsep:
* **Simulasi Lokal:** Komunikasi data saat ini hanya berjalan di *localhost* atau jaringan lokal, belum via Cloud/Internet publik.
* **Direct Socket:** Belum menggunakan *Message Broker* (seperti Kafka/RabbitMQ), sehingga risiko data hilang (*packet loss*) masih ada jika server down.
* **Keamanan:** Data dikirim dalam format JSON biasa (belum terenkripsi/SSL).
* **Single Device:** Saat ini dioptimalkan untuk mensimulasikan satu alat monitor saja.

## 🔮 Future Development Plans
Rencana pengembangan untuk mengubah simulasi ini menjadi produk *production-ready*:
-  **Message Broker Integration:** Implementasi Apache Kafka/RabbitMQ untuk menangani antrian data bervolume tinggi.
-  **HL7 Standard:** Adopsi standar format data kesehatan internasional (HL7/FHIR).
-  **Security:** Menambahkan enkripsi SSL/TLS pada komunikasi socket.
-  **Cloud Deployment:** Deploy sistem ke AWS (EC2) atau Google Cloud Platform.
-  **Multi-Device Support:** Mengembangkan server agar mampu menangani ribuan *concurrent connections* (AsyncIO).

## 👤 Author
**Rafli Firmansyah**
> *Project ini dibangun untuk mendemonstrasikan kemampuan System Integration, Network Programming, dan Database Administration dalam konteks teknologi kesehatan.*

## 📝 License
Proyek ini ditujukan untuk **penggunaan edukasi** dan **portofolio profesional**.

## 📞 Support
Jika ada pertanyaan teknis mengenai arsitektur atau kode, silakan hubungi penulis via **LinkedIn**.
