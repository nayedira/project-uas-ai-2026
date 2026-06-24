import os
import streamlit as st
import time
import re
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EDUSIST - Exhibition", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    html, body, [class*="css"], .stTextInput input, .stSelectbox, .stMarkdown, p, h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        letter-spacing: -0.015em;
    }
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
        background-image: radial-gradient(rgba(56, 77, 149, 0.15) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(56, 77, 149, 0.1);
    }
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(135deg, #384d95 0%, #e63e88 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 12px 24px;
        box-shadow: 0 4px 15px rgba(56, 77, 149, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(56, 77, 149, 0.4);
    }
    button[kind="primary"] {
        background: #e63e88 !important;
        box-shadow: 0 4px 15px rgba(230, 62, 136, 0.3) !important;
    }
    .gradient-text {
        background: linear-gradient(to right, #384d95, #e63e88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
        text-align: center;
    }
    .subtitle-text {
        text-align: center;
        color: var(--text-color);
        opacity: 0.8;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .login-box {
        background: var(--secondary-background-color);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(56, 77, 149, 0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 20px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    .stChatMessage {
        background-color: var(--secondary-background-color);
        border-radius: 18px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        border: 1px solid rgba(56, 77, 149, 0.1);
        margin-bottom: 15px;
    }
    [data-testid="stDialog"] {
        border-radius: 24px;
        padding: 20px;
        background-color: var(--secondary-background-color);
    }
    .stChatInputContainer textarea::placeholder {
        color: rgba(128, 128, 128, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTO DETECT SUBJECT FUNCTION ---
def auto_detect_mapel(text):
    text = text.lower()
    if any(w in text for w in ["hitung", "rumus", "angka", "matematika", "persamaan", "kuadrat", "akar", "tambah", "kurang", "kali", "bagi", "x", "y", "peluang", "trigonometri", "math", "calculate", "formula", "equation"]): return "Mathematics"
    if any(w in text for w in ["sel", "hewan", "tumbuhan", "biologi", "fotosintesis", "dna", "bakteri", "virus", "jaringan", "organ", "cell", "animal", "plant", "biology", "mitosis", "bacteriofag"]): return "Science"
    if any(w in text for w in ["gaya", "cepat", "fisika", "gravitasi", "newton", "energi", "joule", "listrik", "magnet", "kecepatan", "physics", "force", "speed", "energy", "velocity"]): return "Physics"
    if any(w in text for w in ["atom", "reaksi", "kimia", "unsur", "senyawa", "asam", "basa", "molekul", "ikatan", "larutan", "chemistry", "reaction", "element"]): return "Chemistry"
    return "General"

# --- 2. SETUP SESSION STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "kelas_siswa" not in st.session_state: st.session_state.kelas_siswa = "Grade 10"
if "chat_sessions" not in st.session_state: st.session_state.chat_sessions = {"Session 1": {"subject": None, "messages": []}}
if "active_chat" not in st.session_state: st.session_state.active_chat = "Session 1"
if "show_popup" not in st.session_state: st.session_state.show_popup = False

# --- POP-UP MODAL FUNCTION ---
@st.dialog("Welcome to EDUSIST")
def onboarding_popup():
    st.write(f"Hello **{st.session_state.user_name}**!")
    st.write("Type your question below, and I will **automatically detect** the subject. You can also select it manually in the sidebar.")
    st.write("")
    if st.button("Start Chatting", use_container_width=True):
        st.session_state.show_popup = False 
        st.rerun()

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='gradient-text'>EDUSIST</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle-text'>AI-Powered Ethical Education System</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.subheader("Let's Start Learning")
        st.write("Fill out your profile below to get started.")
        st.write("") 
        
        nama_input = st.text_input("Nickname:", placeholder="Type your name here...")
        kelas_input = st.selectbox("Grade Level:", ["Grade 10", "Grade 11", "Grade 12"])
        
        st.write("") 
        if st.button("Next", use_container_width=True):
            if nama_input.strip() == "":
                st.error("Name cannot be empty.")
            else:
                st.session_state.user_name = nama_input
                st.session_state.kelas_siswa = kelas_input
                st.session_state.logged_in = True
                st.session_state.show_popup = True 
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. MAIN CHAT ROOM ---
else:
    if st.session_state.show_popup:
        onboarding_popup()

    # SIDEBAR SETUP
    with st.sidebar:
        st.markdown("<h1 class='gradient-text' style='font-size:2rem;'>EDUSIST</h1>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown(f"🧑‍🎓 **{st.session_state.user_name}**")
        new_grade = st.selectbox("Grade Level:", ["Grade 10", "Grade 11", "Grade 12"], index=["Grade 10", "Grade 11", "Grade 12"].index(st.session_state.kelas_siswa), label_visibility="collapsed")
        if new_grade != st.session_state.kelas_siswa:
            st.session_state.kelas_siswa = new_grade
            st.rerun()
            
        st.divider()
        mapel_container = st.empty()
        st.divider()
        
        st.markdown("### Learning History")
        if st.button("Create New Session", use_container_width=True):
            new_chat_id = f"Session {len(st.session_state.chat_sessions) + 1}"
            st.session_state.chat_sessions[new_chat_id] = {"subject": None, "messages": []}
            st.session_state.active_chat = new_chat_id
            st.rerun()
            
        chat_list = list(st.session_state.chat_sessions.keys())
        current_index = chat_list.index(st.session_state.active_chat)
        selected_chat = st.selectbox("Select Session:", chat_list, index=current_index, label_visibility="collapsed")
        
        if selected_chat != st.session_state.active_chat:
            st.session_state.active_chat = selected_chat
            st.rerun()

        st.divider()
        if st.button("Leave Class", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.chat_sessions = {"Session 1": {"subject": None, "messages": []}}
            st.session_state.active_chat = "Session 1"
            st.session_state.show_popup = False
            st.rerun()

    active_chat_data = st.session_state.chat_sessions[st.session_state.active_chat]
    curr_subj = active_chat_data["subject"]
    active_messages = active_chat_data["messages"]
    
    st.markdown("<h2 style='color:#384d95; font-weight:800;'>Interactive Learning Room</h2>", unsafe_allow_html=True)
    if curr_subj is None or curr_subj == "Auto-Detect":
        st.caption(f"Session: **{st.session_state.active_chat}** | Subject: *Auto-Detect Mode...*")
    else:
        st.caption(f"Session: **{st.session_state.active_chat}** | Subject: **{curr_subj}**")

    if not active_messages and not st.session_state.show_popup:
        with st.chat_message("assistant"):
            if curr_subj is None or curr_subj == "Auto-Detect":
                st.write("Please type your first question below. I will detect the subject automatically.")
            else:
                st.write(f"Class is ready! What would you like to learn about {curr_subj}?")

    for msg in active_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "transparency" in msg:
                with st.expander("AI Guardrails Evaluation Detail"):
                    label = msg["transparency"]["label"]
                    if label == "valid_learning":
                        st.success(f"Label: {label}")
                    elif label in ["cheating_attempt", "inappropriate"]:
                        st.error(f"Label: {label}")
                    elif label == "out_of_context":
                        st.warning(f"Label: {label}")
                    st.write(f"**Reason:** {msg['transparency']['reason']}")
                    st.write(f"**Confidence Score:** {msg['transparency']['confidence']}")

    chat_placeholder = "Type your question here..." if curr_subj is None or curr_subj == "Auto-Detect" else f"Ask about {curr_subj} here..."

    if prompt := st.chat_input(chat_placeholder):
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.chat_sessions[st.session_state.active_chat]["messages"].append({"role": "user", "content": prompt})
        prompt_lower = prompt.lower()
        
        current_session_subject = st.session_state.chat_sessions[st.session_state.active_chat]["subject"]
        if current_session_subject is None or current_session_subject == "Auto-Detect":
            detected_mapel = auto_detect_mapel(prompt_lower)
            st.session_state.chat_sessions[st.session_state.active_chat]["subject"] = detected_mapel
            curr_subj = detected_mapel
            st.toast(f"Subject detected: {detected_mapel}")
        
        # --- GUARDRAILS START ---
        if len(prompt_lower.strip()) < 3 or re.search(r'[^aiueo\s0-9]{5,}', prompt_lower):
            response = "Hmm, your typing seems unclear or contains typos. Let's try asking your question with a proper sentence."
            transparency = {"label": "out_of_context", "reason": "Detected meaningless text (gibberish) or invalid input.", "confidence": "98.1%"}
            
        elif any(w in prompt_lower for w in ["jawaban", "contekan", "answer", "cheat", "key", "kunci"]):
            response = f"Sorry {st.session_state.user_name}, EDUSIST is designed to guide your learning, not to give instant answers. Let's learn the step-by-step process together."
            transparency = {"label": "cheating_attempt", "reason": "Detected a pattern requesting direct answers.", "confidence": "96.5%"}
            
        elif any(w in prompt_lower for w in ["bego", "bodoh", "kasar", "goblok", "tolol", "anjing", "anjay", "stupid", "idiot", "fuck", "shit", "bitch", "asshole"]):
            response = f"Hello {st.session_state.user_name}. Let's keep this classroom positive. Please use polite language so we can learn comfortably."
            transparency = {"label": "inappropriate", "reason": "Detected inappropriate language.", "confidence": "92.8%"}
            
        elif any(w in prompt_lower for w in ["game", "film", "makan", "movie", "food", "play"]):
            response = "That sounds fun, but it is a bit off-topic from school. Let's focus back on the lesson."
            transparency = {"label": "out_of_context", "reason": "Topic is not correlated with school subjects.", "confidence": "89.2%"}
            
        # --- LULUS GUARDRAILS -> BACKEND API.PY ---
        else:
            transparency = {"label": "valid_learning", "reason": "Safe and educational question.", "confidence": "Waiting for API..."}
            
            try:
                api_url = "https://project-uas-ai-2026-production.up.railway.app/generate-answer"
                
                payload = {
                    "pertanyaan": prompt_lower,
                    "mapel": curr_subj
                }
                api_response = requests.post(api_url, json=payload, timeout=60) 
                
                
                if api_response.status_code == 200:
                    hasil = api_response.json()
                    # Menarik jawaban dari Backend
                    response = hasil.get("jawaban", "Model tidak mengembalikan jawaban.")
                    transparency["confidence"] = hasil.get("confidence", "API Active")
                else:
                    response = f"Oops! Error dari API Backend (Status Code: {api_response.status_code})."
                    transparency["confidence"] = "API Error"
                    
            except requests.exceptions.ConnectionError:
                response = "⚠️ Gagal terhubung ke API! Pastikan kamu sudah menyalakan terminal `uvicorn api:app --reload`."
                transparency["confidence"] = "Connection Refused"
            except Exception as e:
                response = f"Terjadi error saat memanggil API: {e}"
                transparency["confidence"] = "Error"

        with st.chat_message("assistant"):
            with st.spinner("Mikirin jawaban dari API Backend..."):
                time.sleep(0.5) 
                st.write(response)
                with st.expander("AI Guardrails Evaluation Detail"):
                    if transparency["label"] == "valid_learning":
                        st.success(f"Label: {transparency['label']}")
                    elif transparency["label"] in ["cheating_attempt", "inappropriate"]:
                        st.error(f"Label: {transparency['label']}")
                    elif transparency["label"] == "out_of_context":
                        st.warning(f"Label: {transparency['label']}")
                    st.write(f"**Reason:** {transparency['reason']}")
                    st.write(f"**Confidence Score:** {transparency['confidence']}")
        
        st.session_state.chat_sessions[st.session_state.active_chat]["messages"].append({
            "role": "assistant",
            "content": response,
            "transparency": transparency
        })
        st.rerun()

    # UPDATE MAPEL SIDEBAR TO ALWAYS SHOW DROPDOWN
    with mapel_container.container():
        st.markdown("### Subjects")
        if st.session_state.kelas_siswa == "Grade 10":
            daftar_mapel = ["Auto-Detect", "General", "Mathematics", "Indonesian", "English", "Science", "Social Studies", "Computer Science"]
        else:
            daftar_mapel = ["Auto-Detect", "General", "Mathematics", "Indonesian", "English", "Biology", "Chemistry", "Physics", "Sociology", "Economics", "Computer Science", "Geography", "History"]
        
        display_subj = curr_subj if curr_subj is not None else "Auto-Detect"
        if display_subj not in daftar_mapel: 
            daftar_mapel.append(display_subj)
            
        new_subj = st.selectbox("Session focus subject:", daftar_mapel, index=daftar_mapel.index(display_subj))
        
        if new_subj != display_subj:
            st.session_state.chat_sessions[st.session_state.active_chat]["subject"] = None if new_subj == "Auto-Detect" else new_subj
            st.rerun()
