import streamlit as st
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="EDUSIST - Pameran", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (EDTECH MODERN THEME) ---
st.markdown("""
<style>
    <style>
    /* 1. APPLE SYSTEM FONT (SAN FRANCISCO) */
    html, body, [class*="css"], .stTextInput input, .stSelectbox, .stMarkdown, p, h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        letter-spacing: -0.015em;
    }

    /* 2. BACKGROUND UTAMA ADAPTIF DENGAN POLA TITIK (DOTS) */
    [data-testid="stAppViewContainer"] {
        /* Hapus warna hardcode, biarkan transparan agar ikut tema Streamlit */
        background-color: transparent;
        /* Gunakan rgba abu-abu netral agar titiknya terlihat di mode terang maupun gelap */
        background-image: radial-gradient(rgba(128, 128, 128, 0.15) 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* 3. STYLING SIDEBAR */
    [data-testid="stSidebar"] {
        /* Menggunakan warna sekunder bawaan tema (Otomatis putih di Light, abu gelap di Dark) */
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(128, 128, 128, 0.1);
    }

    /* 4. TOMBOL MODERN (Tetap warna gradasi karena cocok di dua mode) */
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 12px 24px;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.3) !important;
    }

    /* 5. TEKS JUDUL & SUBJUDUL ADAPTIF */
    .gradient-text {
        background: linear-gradient(to right, #4F46E5, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
        text-align: center;
    }
    
    .subtitle-text {
        text-align: center;
        color: var(--text-color); /* Otomatis hitam/putih */
        opacity: 0.7; /* Efek memudar agar elegan */
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* 6. KOTAK LOGIN GLASSMORPHISM ADAPTIF */
    .login-box {
        background: var(--secondary-background-color); /* Adaptif */
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* 7. STYLING CHAT BUBBLE ADAPTIF */
    .stChatMessage {
        background-color: var(--secondary-background-color); /* Adaptif */
        border-radius: 18px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. SETUP SESSION STATE MULTI-CHAT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "kelas_siswa" not in st.session_state:
    st.session_state.kelas_siswa = "Kelas 10"
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Sesi Belajar 1": []}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Sesi Belajar 1"

# --- 2. HALAMAN LOGIN ---
if not st.session_state.logged_in:
    # Menggunakan kolom untuk menengahkan box di layar wide
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='gradient-text'>EDUSIST</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle-text'>Sistem Edukasi AI Berbasis Etika 🎓</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.subheader("Mulai Belajar Yuk! 👋")
        st.write("Isi profil kamu di bawah ini untuk memulai.")
        st.write("") # Spacer
        
        nama_input = st.text_input("Nama Panggilan:", placeholder="Ketik namamu di sini...")
        kelas_input = st.selectbox("Tingkat Kelas:", ["Kelas 10", "Kelas 11", "Kelas 12"])
        
        st.write("") # Spacer
        if st.button("🚀 Masuk ke Ruang Kelas", use_container_width=True):
            if nama_input.strip() == "":
                st.error("Nama belum diisi nih!")
            else:
                st.session_state.user_name = nama_input
                st.session_state.kelas_siswa = kelas_input
                st.session_state.logged_in = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. HALAMAN CHAT UTAMA ---
else:
    # Header Chat
    st.markdown("<h2 style='color:#4F46E5; font-weight:800;'>Ruang Belajar Interaktif 🚀</h2>", unsafe_allow_html=True)
    st.caption(f"Topik saat ini: **{st.session_state.active_chat}**")
    
    # --- SETUP SIDEBAR ---
    with st.sidebar:
        st.markdown("<h1 class='gradient-text' style='font-size:2rem;'>EDUSIST</h1>", unsafe_allow_html=True)
        st.divider()
        
        st.info(f"🧑‍🎓 **{st.session_state.user_name}**\n\n🏫 {st.session_state.kelas_siswa}")
        st.divider()
        
        # --- FITUR CHAT BARU & RIWAYAT ---
        st.markdown("### 💬 Riwayat Belajar")
        if st.button("➕ Bikin Sesi Baru", use_container_width=True):
            new_chat_id = f"Sesi Belajar {len(st.session_state.chat_sessions) + 1}"
            st.session_state.chat_sessions[new_chat_id] = []
            st.session_state.active_chat = new_chat_id
            st.rerun()
            
        chat_list = list(st.session_state.chat_sessions.keys())
        current_index = chat_list.index(st.session_state.active_chat)
        selected_chat = st.radio("Pilih Sesi:", chat_list, index=current_index, label_visibility="collapsed")
        
        if selected_chat != st.session_state.active_chat:
            st.session_state.active_chat = selected_chat
            st.rerun()

        st.divider()
        st.markdown("### 📚 Mata Pelajaran")
        if st.session_state.kelas_siswa == "Kelas 10":
            daftar_mapel = ["Matematika", "B. Indonesia", "B. Inggris", "IPA", "IPS", "Informatika"]
        else:
            daftar_mapel = ["Matematika", "B. Indonesia", "B. Inggris", "Biologi", "Kimia", "Fisika", "Sosiologi", "Ekonomi", "Informatika", "Geografi", "Sejarah"]
        subject = st.selectbox("Pilih mapel:", daftar_mapel, label_visibility="collapsed")
        
        st.divider()
        if st.button("🚪 Keluar Kelas", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.chat_sessions = {"Sesi Belajar 1": []}
            st.session_state.active_chat = "Sesi Belajar 1"
            st.rerun()

    # --- TAMPILKAN RIWAYAT CHAT ---
    active_messages = st.session_state.chat_sessions[st.session_state.active_chat]
    
    # Tampilkan sapaan awal jika sesi masih kosong
    if not active_messages:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(f"Halo {st.session_state.user_name}! Aku EDUSIST, asisten belajarmu. Hari ini kita mau bahas materi **{subject}** apa nih?")

    for msg in active_messages:
        # Menambahkan Avatar kustom!
        avatar_icon = "🧑‍🎓" if msg["role"] == "user" else "🤖"
        
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.write(msg["content"])
            if "transparency" in msg:
                with st.expander("🔍 Detail Evaluasi Guardrails AI"):
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
    if prompt := st.chat_input(f"Ketik pertanyaan {subject} di sini..."):
        
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.write(prompt)
        
        st.session_state.chat_sessions[st.session_state.active_chat].append({"role": "user", "content": prompt})

        prompt_lower = prompt.lower()
        
        if "jawaban" in prompt_lower or "contekan" in prompt_lower:
            response = f"Maaf ya {st.session_state.user_name}, EDUSIST dirancang untuk membimbingmu belajar, bukan memberikan jawaban instan. Yuk, kita pelajari langkah-langkahnya bareng!"
            transparency = {"label": "cheating_attempt", "reason": "Terdeteksi pola permintaan jawaban langsung.", "confidence": "96.5%"}
        elif "bego" in prompt_lower or "bodoh" in prompt_lower or "kasar" in prompt_lower:
            response = f"Halo {st.session_state.user_name}! Mari kita jaga ruang kelas ini tetap positif. Gunakan bahasa yang sopan ya agar belajarnya makin nyaman."
            transparency = {"label": "inappropriate", "reason": "Terdeteksi penggunaan kata tidak sopan.", "confidence": "92.8%"}
        elif "game" in prompt_lower or "film" in prompt_lower or "makan" in prompt_lower:
            response = "Wah, seru sih pembahasannya, tapi ini agak melenceng dari topik sekolah nih. Yuk kita kembali fokus ke pelajaran!"
            transparency = {"label": "out_of_context", "reason": "Topik tidak berkorelasi dengan materi sekolah.", "confidence": "89.2%"}
        else:
            response = f"Bagus sekali pertanyaanmu! Berdasarkan kurikulum **{st.session_state.kelas_siswa}** untuk **{subject}**, konsep ini dijelaskan sebagai berikut..."
            transparency = {"label": "valid_learning", "reason": "Pertanyaan aman dan edukatif.", "confidence": "99.1%"}

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Sedang berpikir..."):
                time.sleep(1.0) 
                st.write(response)
                
                with st.expander("🔍 Detail Evaluasi Guardrails AI"):
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
        
        st.session_state.chat_sessions[st.session_state.active_chat].append({
            "role": "assistant",
            "content": response,
            "transparency": transparency
        })