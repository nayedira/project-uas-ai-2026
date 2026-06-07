import streamlit as st

def render_chat_message(msg):
    """
    Fungsi untuk merender satu gelembung chat beserta kotak transparansinya (jika ada).
    Parameter 'msg' adalah dictionary yang berisi role, content, dan transparency.
    """
    with st.chat_message(msg["role"]):
        # Tampilkan teks utama (jawaban atau pertanyaan)
        st.write(msg["content"])
        
        # Jika pesan ini dari bot dan memiliki data transparansi, tampilkan expander
        if "transparency" in msg:
            with st.expander("🔍 Detail Evaluasi AI"):
                label = msg["transparency"]["label"]
                
                # Pewarnaan status berdasarkan label etika
                if label == "valid_learning":
                    st.success(f"✅ Label: {label}")
                elif label == "cheating_attempt":
                    st.error(f"🚨 Label: {label}")
                elif label == "inappropriate":
                    st.error(f"🛑 Label: {label}")
                elif label == "out_of_context":
                    st.warning(f"⚠️ Label: {label}")
                
                # Menampilkan alasan dan skor dari model
                st.write(f"**Alasan:** {msg['transparency']['reason']}")
                st.write(f"**Tingkat Keyakinan (Confidence):** {msg['transparency']['confidence']}")