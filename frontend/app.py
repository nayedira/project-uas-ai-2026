import streamlit as st
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="ChatMOM - Mockup", page_icon="🤖", layout="centered")

st.title("🤖 ChatMOM")
st.markdown("**(Monitored Online Mentoring)** - *Sistem Edukasi AI dengan Ethical Guardrails*")

# --- 1. SETUP SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "kelas_siswa" not in st.session_state:
    st.session_state.kelas_siswa = None

# --- 2. HALAMAN PEMILIHAN KELAS ---
if st.session_state.kelas_siswa is None:
    st.markdown("---")
    st.subheader("👋 Halo! Selamat datang di ChatMOM.")
    st.write("Sebelum mulai belajar, yuk kasih tahu ChatMOM kamu sekarang kelas berapa:")
    
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
        st.header("👤 Profil Siswa")
        st.success(f"🎓 Aktif: **{st.session_state.kelas_siswa}**")
        
        if st.button("🔄 Ganti Kelas"):
            st.session_state.kelas_siswa = None
            st.session_state.messages = [] # Reset riwayat chat
            st.rerun()
            
        st.divider()
        
        st.header("📚 Personalisasi Mapel")
        
        if st.session_state.kelas_siswa == "Kelas 10":
            daftar_mapel = [
                "Matematika", "B. Indonesia", "B. Inggris", 
                "IPA", "IPS", "Informatika"
            ]
        else: # Untuk Kelas 11 dan Kelas 12
            daftar_mapel = [
                "Matematika", "B. Indonesia", "B. Inggris", 
                "Biologi", "Kimia", "Fisika", 
                "Sosiologi", "Ekonomi", "Informatika", 
                "Geografi", "Sejarah"
            ]
            
        # Selectbox sekarang isinya mengikuti daftar_mapel di atas
        subject = st.selectbox("Pilih Mata Pelajaran:", daftar_mapel)
        
        st.divider()
        st.info("💡 **Tips Uji Coba UI:**\n\n"
                "- Ketik kata **'jawaban'** untuk tes filter nyontek.\n"
                "- Ketik kata **'game'** untuk tes filter di luar konteks.\n"
                "- Ketik pertanyaan normal untuk tes valid learning.")

    # --- TAMPILKAN RIWAYAT CHAT ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "transparency" in msg:
                with st.expander("🔍 Lihat Transparansi AI"):
                    label = msg["transparency"]["label"]
                    if label == "valid_learning":
                        st.success(f"✅ Status: {label}")
                    elif label == "cheating_attempt":
                        st.error(f"🚨 Status: {label}")
                    elif label == "out_of_context":
                        st.warning(f"⚠️ Status: {label}")
                    
                    st.write(f"**Alasan:** {msg['transparency']['reason']}")
                    st.write(f"**Confidence Score:** {msg['transparency']['confidence']}")

    # --- INPUT USER & LOGIKA MOCKUP ---
    if prompt := st.chat_input(f"Tanya materi {subject} {st.session_state.kelas_siswa} di sini..."):
        
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        prompt_lower = prompt.lower()
        
        if "jawaban" in prompt_lower or "contekan" in prompt_lower:
            response = "Maaf, ChatMOM tidak bisa memberikan jawaban instan. Mari kita bahas konsep dan cara mengerjakannya bersama-sama ya!"
            transparency = {"label": "cheating_attempt", "reason": "Mendeteksi indikasi meminta jawaban instan.", "confidence": "96.5%"}
        elif "game" in prompt_lower or "film" in prompt_lower:
            response = "Sepertinya pertanyaanmu di luar topik pelajaran kita. Yuk, kembali fokus ke materi sekolah!"
            transparency = {"label": "out_of_context", "reason": "Topik tidak relevan dengan konteks akademik.", "confidence": "89.2%"}
        else:
            response = f"Pertanyaan yang bagus! Karena kamu memilih **{subject}** untuk **{st.session_state.kelas_siswa}**, ChatMOM akan menjelaskan sesuai kurikulum yang tepat."
            transparency = {"label": "valid_learning", "reason": "Pertanyaan aman dan relevan.", "confidence": "99.1%"}

        with st.chat_message("assistant"):
            with st.spinner("Mengevaluasi etika pertanyaan..."):
                time.sleep(1.5) 
                st.write(response)
                
                with st.expander("🔍 Lihat Transparansi AI"):
                    if transparency["label"] == "valid_learning":
                        st.success(f"✅ Status: {transparency['label']}")
                    elif transparency["label"] == "cheating_attempt":
                        st.error(f"🚨 Status: {transparency['label']}")
                    elif transparency["label"] == "out_of_context":
                        st.warning(f"⚠️ Status: {transparency['label']}")
                    
                    st.write(f"**Alasan:** {transparency['reason']}")
                    st.write(f"**Confidence Score:** {transparency['confidence']}")
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "transparency": transparency
        })