import os
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv # <-- Tambahkan ini

# Muat variabel rahasia dari file .env
load_dotenv()

app = FastAPI(title="EDUSIST Gemini Backend API")

# --- 1. KONFIGURASI GEMINI API ---
# Ambil API Key dari environment (sistem operasi)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validasi keamanan: Pastikan kunci ditemukan
if not GEMINI_API_KEY:
    raise ValueError("API Key tidak ditemukan! Pastikan file .env sudah diisi.")

# Daftarkan API Key ke library Google
genai.configure(api_key=GEMINI_API_KEY)

# Pilih model Gemini 
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. FORMAT DATA DARI FRONTEND ---
class ChatRequest(BaseModel):
    pertanyaan: str
    mapel: str

# --- 3. PROSES PENERIMAAN & PENGIRIMAN KE GEMINI ---
@app.post("/generate-answer")
def get_ai_response(request: ChatRequest):
    pertanyaan_user = request.pertanyaan
    mapel_user = request.mapel
    
    try:
        # Kita merancang "Prompt Engineering" agar Gemini bertindak sebagai EDUSIST
        system_prompt = (
            f"Kamu adalah EDUSIST, asisten belajar AI untuk siswa sekolah yang ramah, "
            f"sopan, dan pintar. Berikan penjelasan yang mudah dipahami.\n\n"
            f"Mata Pelajaran: {mapel_user}\n"
            f"Pertanyaan Siswa: {pertanyaan_user}"
        )
        
        # Kirim prompt ke Gemini
        response = model.generate_content(system_prompt)
        
        # Ambil teks jawaban dari Gemini
        jawaban_ai = response.text
        
    except Exception as e:
        # Jika kuota API habis atau internet mati
        jawaban_ai = f"Waduh, koneksi EDUSIST ke server sedang gangguan nih. Detail error: {e}"
    
    return {"jawaban": jawaban_ai}