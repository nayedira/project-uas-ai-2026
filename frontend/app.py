import streamlit as st
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="EDUSIST - Pameran", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (TEMA BUKU TULIS GRADASI) ---
st.markdown("""
<style>
    /* Background area utama */
    [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6;
        background-image: 
            linear-gradient(135deg, rgba(238, 242, 255, 0.95) 0%, rgba(224, 231, 255, 0.85) 100%),
            repeating-linear-gradient(transparent, transparent 31px, rgba(165, 180, 252, 0.4) 31px, rgba(165, 180, 252, 0.4) 32px);
        background-attachment: fixed;
    }

    /* Styling tombol outline */
    .stButton>button {
        border-radius: 12px;
        border: 2px solid #4F46E5 !important;
        background-color: rgba(255, 255, 255, 0.5) !important;
        color: #4F46E5 !important;
        font-weight: 700;
        transition: all 0.3s ease;
        padding: 10px 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .stButton>button:hover {
        background-color: #4F46E5 !important;
        color: #ffffff !important;
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.3);
        transform: translateY(-2px);
    }
    
    /* Styling radio button untuk list history chat */
    .stRadio label {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 5px 10px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. SETUP SESSION STATE DENGAN MULTI-CHAT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "kelas_siswa" not in st.session_state:
    st.session_state.kelas_siswa = "Kelas 10"

# Lemari untuk menyimpan banyak sesi chat
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Obrolan 1": []}
# Penanda chat mana yang sedang dibuka
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Obrolan 1"

# --- 2. HALAMAN LOGIN ---
if not st.session_state.logged_in:
    st.title("🎓 EDUSIST")
    st.markdown("*Sistem Edukasi AI dengan Ethical Guardrails*")
    st.divider()
    
    st.subheader("Selamat datang! 👋")
    st.write("Silakan isi data diri untuk mencoba prototipe pembelajaran adaptif.")
    
    nama_input = st.text_input("Nama Kamu:", placeholder="Ketik nama panggilanmu...")
    kelas_input = st.selectbox("Tingkat Kelas:", ["Kelas 10", "Kelas 11", "Kelas 12"])
    
    if st.button("🚀 Mulai Belajar", use_container_width=True):
        if nama_input.strip() == "":
            st.error("Nama tidak boleh kosong ya!")
        else:
            st.session_state.user_name = nama_input
            st.session_state.kelas_siswa = kelas_input
            st.session_state.logged_in = True
            st.rerun()

# --- 3. HALAMAN CHAT UTAMA ---
else:
    st.title(f"🎓 EDUSIST - {st.session_state.active_chat}")
    
    # --- SETUP SIDEBAR ---
    with st.sidebar:
        st.success(f"👋 Halo, **{st.session_state.user_name}**!\n\n🎓 Status: **{st.session_state.kelas_siswa}**")
        st.divider()
        
        # --- FITUR CHAT BARU & RIWAYAT ---
        st.header("💬 Riwayat Chat")
        
        # Tombol Bikin Chat Baru
        if st.button("➕ Chat Baru", use_container_width=True):
            new_chat_id = f"Obrolan {len(st.session_state.chat_sessions) + 1}"
            st.session_state.chat_sessions[new_chat_id] = [] # Buat keranjang kosong baru
            st.session_state.active_chat = new_chat_id       # Pindah ke chat baru itu
            st.rerun()
            
        # Daftar Radio Button untuk milih chat lama
        chat_list = list(st.session_state.chat_sessions.keys())
        # Memastikan pilihan radio button sesuai dengan chat yang sedang aktif
        current_index = chat_list.index(st.session_state.active_chat)
        
        selected_chat = st.radio("Pilih Sesi:", chat_list, index=current_index)
        
        # Jika user mengklik sesi lain di radio button, pindah haluan!
        if selected_chat != st.session_state.active_chat:
            st.session_state.active_chat = selected_chat
            st.rerun()

        st.divider()
        st.header("📚 Mata Pelajaran")
        if st.session_state.kelas_siswa == "Kelas 10":
            daftar_mapel = ["Matematika", "B. Indonesia", "B. Inggris", "IPA", "IPS", "Informatika"]
        else:
            daftar_mapel = ["Matematika", "B. Indonesia", "B. Inggris", "Biologi", "Kimia", "Fisika", "Sosiologi", "Ekonomi", "Informatika", "Geografi", "Sejarah"]
        subject = st.selectbox("Fokus belajarmu hari ini:", daftar_mapel)
        
        st.divider()
        if st.button("🚪 Akhiri Sesi (Logout)", type="primary", use_container_width=True):
            # Reset HANYA JIKA pengunjung mau ganti orang
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.chat_sessions = {"Obrolan 1": []}
            st.session_state.active_chat = "Obrolan 1"
            st.rerun()

    # --- TAMPILKAN RIWAYAT CHAT (KHUSUS SESI YANG AKTIF SAJA) ---
    active_messages = st.session_state.chat_sessions[st.session_state.active_chat]
    
    for msg in active_messages:
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
                    st.write(f"**Keyakinan (Confidence):** {msg['transparency']['confidence']}")

    # --- INPUT USER ---
    if prompt := st.chat_input(f"Tanyakan materi {subject} di sini..."):
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Simpan pesan user ke keranjang chat yang sedang aktif
        st.session_state.chat_sessions[st.session_state.active_chat].append({"role": "user", "content": prompt})

        prompt_lower = prompt.lower()
        
        if "jawaban" in prompt_lower or "contekan" in prompt_lower:
            response = f"Maaf ya {st.session_state.user_name}, EDUSIST dirancang untuk membimbingmu belajar, bukan memberikan jawaban instan. Yuk, kita pelajari bareng!"
            transparency = {"label": "cheating_attempt", "reason": "Terdeteksi pola permintaan jawaban langsung.", "confidence": "96.5%"}
        elif "bego" in prompt_lower or "bodoh" in prompt_lower or "kasar" in prompt_lower:
            response = f"Halo {st.session_state.user_name}! Mari kita jaga lingkungan belajar ini tetap positif. Gunakan bahasa yang sopan ya."
            transparency = {"label": "inappropriate", "reason": "Terdeteksi penggunaan kata tidak sopan.", "confidence": "92.8%"}
        elif "game" in prompt_lower or "film" in prompt_lower or "makan" in prompt_lower:
            response = "Wah, pembahasannya melenceng dari topik akademik nih. Yuk kembali fokus ke materi pelajaran!"
            transparency = {"label": "out_of_context", "reason": "Topik tidak berkorelasi dengan materi sekolah.", "confidence": "89.2%"}
        else:
            response = f"Bagus sekali pertanyaanmu! Sesuai kurikulum **{st.session_state.kelas_siswa}** untuk **{subject}**, konsep ini dijelaskan sebagai berikut..."
            transparency = {"label": "valid_learning", "reason": "Pertanyaan aman dan edukatif.", "confidence": "99.1%"}

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
                    st.write(f"**Keyakinan (Confidence):** {transparency['confidence']}")
        
        # Simpan balasan AI ke keranjang chat yang sedang aktif
        st.session_state.chat_sessions[st.session_state.active_chat].append({
            "role": "assistant",
            "content": response,
            "transparency": transparency
        })