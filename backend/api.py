from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="EDUSIST Gemini Backend API")

# --- 1. KONFIGURASI GEMINI API ---
# PENTING: Ganti tulisan di bawah dengan API Key asli dari Google AI Studio milikmu
GEMINI_API_KEY = "" 

# Daftarkan API Key ke library Google
genai.configure(api_key=GEMINI_API_KEY)

# Pilih model Gemini (gemini-1.5-flash adalah yang paling cepat dan cerdas untuk chatbot)
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