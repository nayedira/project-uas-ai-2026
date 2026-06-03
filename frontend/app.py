import streamlit as st
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="EDUSIST - Mockup", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (MENGADOPSI GAYA PELAJARI.AI / EDTECH MODERN) ---
st.markdown("""
<style>
    /* Styling untuk tombol agar terlihat lebih modern (rounded) */
    .stButton>button {
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #333333;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 10px 24px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        border-color: #4CAF50;
        color: #4CAF50;
        box-shadow: 0 4px 10px rgba(76, 175, 80, 0.2);
    }
    
    /* Styling header */
    h1 {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    /* Mengubah warna background sidebar agar lebih soft */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER APLIKASI ---
st.title("🎓 EDUSIST")
st.markdown("**Education Assistant** • *Sistem Edukasi AI dengan Ethical Guardrails*")

# --- 1. SETUP SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "kelas_siswa" not in st.session_state:
    st.session_state.kelas_siswa = None

# --- 2. HALAMAN PEMILIHAN KELAS (ONBOARDING DASHBOARD) ---
if st.session_state.kelas_siswa is None:
    st.write("---")
    st.subheader("👋 Halo! Selamat datang di EDUSIST.")
    st.write("Pilih jenjang kelasmu untuk memulai *personalized learning path*:")
    
    st.write("") # Spacer
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏫 SMA Kelas 10", use_container_width=True):
            st.session_state.kelas_siswa = "Kelas 10"
            st.rerun()
            
    with col2:
        if st.button("🏫 SMA Kelas 11", use_container_width=True):
            st.session_state.kelas_siswa = "Kelas 11"
            st.rerun()
            
    with col3:
        if st.button("🏫 SMA Kelas 12", use_container_width=True):
            st.session_state.kelas_siswa = "Kelas 12"
            st.rerun()

# --- 3. HALAMAN CHAT UTAMA ---
else:
    # --- SETUP SIDEBAR & LOGIKA MAPEL DINAMIS ---
    with st.sidebar:
        st.header("👤 Profil Belajar")
        st.success(f"🎓 Status: **{st.session_state.kelas_siswa}**")
        
        if st.button("🔄 Ganti Kelas / Reset"):
            st.session_state.kelas_siswa = None
            st.session_state.messages = [] 
            st.rerun()
            
        st.divider()
        
        st.header("📚 Pilih Mata Pelajaran")
        
        # LOGIKA DAFTAR PELAJARAN BERDASARKAN KELAS
        if st.session_state.kelas_siswa == "Kelas 10":
            daftar_mapel = ["Matematika", "B. Indonesia", "B. Inggris", "IPA", "IPS", "Informatika"]
        else:
            daftar_mapel = ["Matematika", "B. Indonesia", "B. Inggris", "Biologi", "Kimia", "Fisika", "Sosiologi", "Ekonomi", "Informatika", "Geografi", "Sejarah"]
            
        subject = st.selectbox("Fokus belajarmu hari ini:", daftar_mapel)
        
        st.divider()
        st.caption("💡 **Uji Coba Ethical Guardrails:**")
        st.caption("- Ketik **'jawaban'** (Tes Nyontek)")
        st.caption("- Ketik **'bego'** (Tes Toxic)")
        st.caption("- Ketik **'game'** (Tes OOT)")
        st.caption("- Ketik **'rumus'** (Tes Belajar)")

    # --- TAMPILKAN RIWAYAT CHAT ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "transparency" in msg:
                with st.expander("🔍 Detail Evaluasi AI"):
                    label = msg["transparency"]["label"]
                    if label == "valid_learning":
                        st.success(f"✅ Label: {label}")
                    elif label == "cheating_attempt":
                        st.error(f"🚨 Label: {label}")
                    elif label == "inappropriate":
                        st.error(f"🛑 Label: {label}")
                    elif label == "out_of_context":
                        st.warning(f"⚠️ Label: {label}")
                    
                    st.write(f"**Alasan:** {msg['transparency']['reason']}")
                    st.write(f"**Tingkat Keyakinan (Confidence):** {msg['transparency']['confidence']}")

    # --- INPUT USER & LOGIKA KLASIFIKASI MOCKUP ---
    if prompt := st.chat_input(f"Tanyakan materi {subject} di sini..."):
        
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        prompt_lower = prompt.lower()
        
        # 1. Deteksi Cheating
        if "jawaban" in prompt_lower or "contekan" in prompt_lower:
            response = "Maaf ya, EDUSIST dirancang untuk membimbingmu belajar, bukan sekadar memberikan jawaban instan. Yuk, kita pelajari langkah-langkah penyelesaiannya bersama!"
            transparency = {"label": "cheating_attempt", "reason": "Terdeteksi pola permintaan jawaban langsung.", "confidence": "96.5%"}
        
        # 2. Deteksi Inappropriate (Toxic)
        elif "bego" in prompt_lower or "bodoh" in prompt_lower or "kasar" in prompt_lower:
            response = "Halo! Mari kita jaga lingkungan belajar ini tetap positif dan saling menghargai. Gunakan bahasa yang sopan ya."
            transparency = {"label": "inappropriate", "reason": "Terdeteksi penggunaan kata tidak sopan/kasar.", "confidence": "92.8%"}
            
        # 3. Deteksi OOT
        elif "game" in prompt_lower or "film" in prompt_lower or "makan" in prompt_lower:
            response = "Wah, pembahasannya sepertinya melenceng dari topik akademik. Yuk, kita kembali fokus ke materi pelajaranmu!"
            transparency = {"label": "out_of_context", "reason": "Topik tidak memiliki korelasi dengan materi sekolah.", "confidence": "89.2%"}
            
        # 4. Valid Learning
        else:
            response = f"Bagus sekali kamu menanyakan hal ini! Sesuai kurikulum **{st.session_state.kelas_siswa}** untuk mata pelajaran **{subject}**, konsep ini dapat dijelaskan sebagai berikut..."
            transparency = {"label": "valid_learning", "reason": "Pertanyaan teridentifikasi aman dan edukatif.", "confidence": "99.1%"}

        with st.chat_message("assistant"):
            with st.spinner("Menganalisis pertanyaan..."):
                time.sleep(1.2) 
                st.write(response)
                
                with st.expander("🔍 Detail Evaluasi AI"):
                    if transparency["label"] == "valid_learning":
                        st.success(f"✅ Label: {transparency['label']}")
                    elif transparency["label"] == "cheating_attempt":
                        st.error(f"🚨 Label: {transparency['label']}")
                    elif transparency["label"] == "inappropriate":
                        st.error(f"🛑 Label: {transparency['label']}")
                    elif transparency["label"] == "out_of_context":
                        st.warning(f"⚠️ Label: {transparency['label']}")
                    
                    st.write(f"**Alasan:** {transparency['reason']}")
                    st.write(f"**Tingkat Keyakinan (Confidence):** {transparency['confidence']}")
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "transparency": transparency
        })