# EDUSIST 🎓 - AI-Powered Ethical Education System

EDUSIST adalah asisten pembelajaran interaktif berbasis *Artificial Intelligence* yang dirancang untuk membimbing siswa memahami berbagai mata pelajaran. Proyek ini mengusung pendekatan **Hybrid AI**, menggabungkan Model Machine Learning Lokal (PyTorch) untuk klasifikasi & verifikasi (*Guardrails*), serta Gemini API untuk *generative response* yang natural.

Proyek ini dibangun menggunakan arsitektur **Client-Server (Microservices)**:
- **Frontend:** Streamlit (UI Interaktif)
- **Backend:** FastAPI (AI Logic, Model ML Lokal, & Integrasi Gemini API)

---

## 📂 Struktur Direktori Utama

```text
PROJECT-UAS-AI-2026/
├── backend/
│   ├── Model/                 # Folder berisi model PyTorch lokal (.safetensors, dll)
│   ├── api.py                 # File utama backend (FastAPI)
│   ├── .env                   # File konfigurasi rahasia (API Key) -> Jangan di-push!
│   └── requirements.txt       # Library khusus backend
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml        # Konfigurasi tema warna UI
│   ├── app.py                 # File utama frontend (Streamlit)
│   └── requirements.txt       # Library khusus frontend
├── .gitignore                 # Daftar file yang diabaikan oleh Git
└── README.md                  # Dokumentasi proyek