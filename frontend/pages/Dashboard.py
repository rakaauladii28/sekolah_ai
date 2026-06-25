import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI School Future",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_URL}/api"

# =========================================================
# GUARD LOGIN
# =========================================================
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Kamu belum login! Silakan login terlebih dahulu.")
    st.switch_page("Login.py")
    st.stop()

# =========================================================
# DATA USER
# =========================================================
user_data = st.session_state.user
nama_user = user_data.get("nama_lengkap", "Siswa")
user_id = user_data.get("id")

# =========================================================
# INIT SESSION STATE
# =========================================================
defaults = {
    "chat_history": None,
    "current_chat": "Percakapan Utama",
    "is_loading": False,
    "last_user_message": "",
    "tryout_started": False,
    "tryout_questions": [],
    "tryout_answers": [],
    "selected_kampus": [],
    "selected_jurusan": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# FUNCTIONS
# =========================================================
def load_riwayat_dari_db():
    try:
        res = requests.get(f"{API_URL}/chat/riwayat/{user_id}")
        data = res.json()

        if data.get("status") == "success" and data.get("data"):
            messages = []
            for item in data["data"]:
                messages.append({
                    "role": "user",
                    "content": item["pesan_user"]
                })
                if item.get("respons_ai"):
                    messages.append({
                        "role": "assistant",
                        "content": item["respons_ai"]
                    })
            return messages
    except Exception as e:
        print("ERROR LOAD RIWAYAT:", e)

    return None


def load_riwayat_assessment(user_id):
    try:
        res = requests.get(f"{API_URL}/assessment/riwayat/{user_id}")
        data = res.json()
        if data.get("status") == "success":
            return data.get("data", [])
    except Exception as e:
        print("ERROR LOAD ASSESSMENT:", e)

    return []


# =========================================================
# LOAD CHAT HISTORY AWAL
# =========================================================
if st.session_state.chat_history is None:
    riwayat = load_riwayat_dari_db()

    if riwayat:
        st.session_state.chat_history = {
            "Percakapan Utama": riwayat
        }
    else:
        st.session_state.chat_history = {
            "Percakapan Utama": [
                {
                    "role": "assistant",
                    "content": f"Halo {nama_user}! Yuk mulai tanya tentang jurusan, karir, atau masa depan kamu 🚀"
                }
            ]
        }

# jaga current_chat valid
if (
    st.session_state.current_chat is None
    or st.session_state.current_chat not in st.session_state.chat_history
):
    st.session_state.current_chat = "Percakapan Utama"

messages = st.session_state.chat_history[st.session_state.current_chat]


# =========================================================
# CSS / THEME DASHBOARD — RESPONSIVE FIXED
# =========================================================
st.markdown("""
<style>
    /* =========================================
       FORCE COLOR SCHEME GLOBAL
    ========================================= */
    :root {
        color-scheme: dark !important;
    }

    /* =========================================
       APP / BACKGROUND UTAMA
    ========================================= */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: linear-gradient(180deg, #071225 0%, #0b1730 100%) !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* =========================================
       BLOCK CONTAINER — RESPONSIVE PADDING
    ========================================= */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: clamp(0.75rem, 3vw, 2.5rem) !important;
        padding-right: clamp(0.75rem, 3vw, 2.5rem) !important;
        max-width: 100% !important;
    }

    /* =========================================
       TEXT AREA UTAMA — DIKUNCI TETAP PUTIH
    ========================================= */
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6,
    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label,
    [data-testid="stMain"] li {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stat-value,
    .stat-label,
    .section-title,
    .section-subtitle {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stMain"] .stCaption,
    [data-testid="stMain"] .stCaption span,
    [data-testid="stMain"] small {
        color: #cbd5e1 !important;
        -webkit-text-fill-color: #cbd5e1 !important;
    }

    /* =========================================
       SIDEBAR — DIKUNCI TERANG
    ========================================= */
    section[data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #dbe2ea !important;
        /* Lebar sidebar lebih ramping di layar kecil */
        min-width: clamp(200px, 22vw, 280px) !important;
        max-width: clamp(200px, 22vw, 280px) !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] a {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] * {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
    }

    /* =========================================
       INPUT / SELECTBOX / MULTISELECT
    ========================================= */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    .stTextArea textarea {
        background: #f8fafc !important;
        border: 1px solid #dbe2ea !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    [data-testid="stMain"] div[data-baseweb="input"] input,
    [data-testid="stMain"] .stTextArea textarea,
    [data-testid="stMain"] div[data-baseweb="select"] *,
    [data-testid="stMain"] div[role="listbox"] *,
    [data-testid="stMain"] div[role="option"] * {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    div[data-baseweb="input"] input::placeholder,
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 1 !important;
    }

    div[role="listbox"] {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #dbe2ea !important;
    }

    div[role="option"] {
        background: #ffffff !important;
    }

    div[role="option"]:hover {
        background: #eff6ff !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background: #ef4444 !important;
        border-radius: 8px !important;
    }

    .stMultiSelect [data-baseweb="tag"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* =========================================
       TABS
    ========================================= */
    [data-baseweb="tab-list"] {
        gap: clamp(4px, 1.5vw, 10px);
        flex-wrap: wrap;
    }

    [data-baseweb="tab"] {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: clamp(7px, 1.5vw, 10px) clamp(10px, 2.5vw, 18px) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    [data-baseweb="tab"] div,
    [data-baseweb="tab"] span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: clamp(13px, 2vw, 15px) !important;
    }

    [aria-selected="true"][data-baseweb="tab"] {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%) !important;
        border: none !important;
    }

    [aria-selected="true"][data-baseweb="tab"] * {
        font-weight: 700 !important;
    }

    /* =========================================
       STAT CARDS — RESPONSIVE GRID
    ========================================= */
    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: clamp(14px, 3vw, 20px);
        text-align: center;
        margin-bottom: 8px;
    }

    .stat-icon {
        font-size: clamp(1.4rem, 3vw, 1.8rem);
        margin-bottom: 6px;
    }

    .stat-value {
        font-size: clamp(1.4rem, 3.5vw, 2rem);
        font-weight: 800;
        margin-bottom: 4px;
    }

    .stat-label {
        font-size: clamp(11px, 1.8vw, 13px);
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* =========================================
       PANEL CARD
    ========================================= */
    .panel-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: clamp(14px, 3vw, 20px);
        margin-bottom: 16px;
    }

    .section-title {
        font-size: clamp(1rem, 2.5vw, 1.25rem);
        font-weight: 700;
        margin-bottom: 6px;
    }

    .section-subtitle {
        font-size: clamp(12px, 1.8vw, 14px);
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* =========================================
       CHAT BUBBLE
    ========================================= */
    .chat-wrapper {
        width: 100%;
        max-width: 850px;
        margin: auto;
        padding: 10px 0 20px;
    }

    .chat-row {
        display: flex;
        margin-bottom: 12px;
    }

    .chat-user { justify-content: flex-end; }
    .chat-ai   { justify-content: flex-start; }

    .bubble {
        padding: clamp(10px, 2vw, 12px) clamp(12px, 2.5vw, 16px);
        border-radius: 18px;
        max-width: 90%;
        font-size: clamp(13px, 2vw, 15px);
        line-height: 1.5;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .user-bubble {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        border-bottom-right-radius: 4px;
    }

    .user-bubble * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .ai-bubble {
        background: #ffffff !important;
        border-bottom-left-radius: 4px;
    }

    .ai-bubble,
    .ai-bubble *,
    .ai-bubble p,
    .ai-bubble span,
    .ai-bubble div {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    /* =========================================
       CARD CONTAINER BOX
    ========================================= */
    [data-testid="stForm"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 18px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
    }

    /* =========================================
       ALERT & PROGRESS
    ========================================= */
    [data-testid="stAlert"] * {
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%) !important;
    }

    /* =========================================
       CHAT INPUT
    ========================================= */
    [data-testid="stChatInput"] textarea {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        background: #f8fafc !important;
        font-size: clamp(13px, 2vw, 15px) !important;
    }

    [data-testid="stChatInput"] {
        background: transparent !important;
    }

    /* =========================================
       MAIN HEADER — RESPONSIVE FONT
    ========================================= */
    [data-testid="stMain"] h1 {
        font-size: clamp(1.4rem, 4vw, 2rem) !important;
    }

    [data-testid="stMain"] h3 {
        font-size: clamp(1rem, 2.5vw, 1.3rem) !important;
    }

    /* =========================================
       MOBILE — ≤ 640px
    ========================================= */
    @media screen and (max-width: 640px) {
        /* Sidebar otomatis collapse di mobile — hanya perkecil padding kalau terbuka */
        section[data-testid="stSidebar"] {
            min-width: 240px !important;
            max-width: 240px !important;
        }

        /* Kolom stats: susun vertikal di mobile */
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .stat-card {
            display: flex;
            align-items: center;
            gap: 14px;
            text-align: left;
            padding: 14px 16px;
        }

        .stat-icon {
            font-size: 1.6rem;
            margin-bottom: 0;
        }

        .stat-value {
            font-size: 1.4rem;
            margin-bottom: 0;
        }

        .bubble {
            max-width: 95%;
        }

        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
    }

    /* =========================================
       TABLET — 641–900px
    ========================================= */
    @media screen and (min-width: 641px) and (max-width: 900px) {
        /* Kolom stats: 2 kolom di tablet */
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 48% !important;
            min-width: 48% !important;
        }

        section[data-testid="stSidebar"] {
            min-width: 210px !important;
            max-width: 210px !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.title("AI School Future")
    st.markdown("---")

    if st.button("+ Percakapan Baru", use_container_width=True, key="new_chat_btn"):
        new_id = len(st.session_state.chat_history) + 1
        new_name = f"Chat {new_id}"
        st.session_state.chat_history[new_name] = [
            {
                "role": "assistant",
                "content": f"Halo {nama_user}! Ada yang ingin kamu tanyakan soal jurusan?"
            }
        ]
        st.session_state.current_chat = new_name
        st.rerun()

    st.markdown("### Riwayat Chat")
    for chat_name in list(st.session_state.chat_history.keys()):
        is_active = chat_name == st.session_state.current_chat
        if st.button(
            chat_name,
            key=f"btn_{chat_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")
    st.write(f"**👤 {nama_user}**")
    st.caption(user_data.get("email", ""))

    if st.button("Logout", use_container_width=True, key="logout_btn"):
        st.session_state.user = None
        st.session_state.chat_history = None
        st.session_state.current_chat = "Percakapan Utama"
        st.switch_page("Login.py")


# =========================================================
# MAIN HEADER
# =========================================================
st.markdown(
    f"""
    <div>
        <h1 style="margin-bottom:0;">Dashboard AI School Future</h1>
        <p style="margin-top:6px; color:#cbd5e1 !important;">
            Selamat datang, <b>{nama_user}</b> 👋
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# STATS
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📑</div>
        <div class="stat-value">{len(st.session_state.chat_history)}</div>
        <div class="stat-label">Total Chat</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">🔥</div>
        <div class="stat-value">Aktif</div>
        <div class="stat-label">Status Akun</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-value">{len(messages)}</div>
        <div class="stat-label">Total Pesan</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================
tab1, tab2 = st.tabs(["💬 Chat AI", "🧠 Tes Minat & Bakat + Tryout"])


# =========================================================
# TAB 1 - CHAT AI
# =========================================================
with tab1:
    st.markdown("""
    <div class="panel-card" style="margin-bottom: 20px;">
        <div class="section-title">🤖 AI Career Assistant</div>
        <div class="section-subtitle">
            Tanyakan jurusan, karir, prospek kerja, atau masa depan kamu di sini.
        </div>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()

    with chat_container:
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if st.session_state.is_loading:
        with st.chat_message("assistant"):
            st.markdown("🤖 *AI sedang menganalisis...*")

    user_input = st.chat_input("💬 Tulis pertanyaan kamu tentang jurusan atau karir...")

    if user_input and not st.session_state.is_loading:
        st.session_state.last_user_message = user_input

        messages.append({
            "role": "user",
            "content": user_input
        })

        st.session_state.chat_history[st.session_state.current_chat] = messages
        st.session_state.is_loading = True
        st.rerun()


# =========================================================
# TAB 2 - TRYOUT + TES MINAT
# =========================================================
with tab2:
    # ================= TRYOUT =================
    st.markdown("""
    <div class="panel-card">
        <div class="section-title">🎯 Tryout Jurusan</div>
        <div class="section-subtitle">
            Pilih jurusan dan kampus tujuan, lalu kerjakan tryout untuk melihat peluang masuk.
        </div>
    """, unsafe_allow_html=True)

    jurusan = st.selectbox(
        "Pilih jurusan",
        [
            "Teknik Informatika",
            "Teknik Industri",
            "Teknik Mesin",
            "Teknik Tekstil",
            "Manajemen Industri"
        ],
        key="jurusan_tryout"
    )

    kampus = st.multiselect(
        "Pilih 2–3 kampus tujuan",
        [
            "UI",
            "ITB",
            "UGM",
            "BINUS",
            "UNPAD",
            "STT Wastukancana"
        ],
        key="kampus_tryout"
    )

    if not st.session_state.tryout_started:
        if st.button("🚀 Mulai Tryout", key="start_tryout_btn", type="primary"):
            if len(kampus) < 2:
                st.warning("Pilih minimal 2 kampus!")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/tryout/start",
                        json={"jurusan": jurusan, "kampus": kampus}
                    )
                    data = res.json()

                    if res.status_code == 200 and data.get("status") == "success":
                        st.session_state.tryout_started = True
                        st.session_state.tryout_questions = data.get("questions", [])
                        st.session_state.selected_kampus = kampus
                        st.session_state.selected_jurusan = jurusan
                        st.rerun()
                    else:
                        st.error(data.get("message", "Gagal memulai tryout."))
                except Exception:
                    st.error("Tidak dapat terhubung ke server tryout.")

    # SOAL TRYOUT
    if st.session_state.tryout_started:
        st.markdown("### 📝 Soal Tryout")

        with st.form("form_tryout"):
            answers = []

            for i, q in enumerate(st.session_state.tryout_questions):
                st.write(f"**{i+1}. {q['question']}**")
                ans = st.radio(
                    "Jawaban:",
                    q["options"],
                    key=f"q_{i}"
                )
                answers.append(ans[0])

            submit_tryout = st.form_submit_button("📊 Submit Hasil Tryout", type="primary")

        if submit_tryout:
            try:
                res = requests.post(
                    f"{API_URL}/tryout/submit",
                    json={
                        "user_answers": answers,
                        "questions": st.session_state.tryout_questions,
                        "kampus": st.session_state.selected_kampus
                    }
                )
                data = res.json()

                if data.get("status") == "success":
                    score = data.get("score", 0)
                    st.success(f"Skor Tryout Kamu: {score}%")

                    if score <= 30:
                        st.warning("""
📚 Jangan menyerah dulu!

Hasil tryout ini bukan akhir, tapi awal untuk berkembang.

**Tips:**
- Pelajari kembali konsep dasar
- Latihan soal rutin
- Fokus pada materi yang masih sulit
- Jangan takut salah saat belajar
                        """)
                    elif score <= 70:
                        st.info("""
🔥 Hasil kamu sudah cukup bagus!

Kamu sudah memahami beberapa materi penting, tinggal ditingkatkan lagi.

**Tips:**
- Kerjakan tryout lebih sering
- Pelajari pembahasan soal yang salah
- Latih manajemen waktu
- Fokus pada kelemahan utama
                        """)
                    else:
                        st.success("""
🏆 Keren banget!

Kemampuan kamu sudah sangat baik dan peluang masuk kampus impian juga besar.

**Tips:**
- Pertahankan konsistensi belajar
- Perbanyak simulasi ujian asli
- Jaga fokus dan mental saat ujian
                        """)

                    st.markdown("### 🎓 Peluang Kampus")
                    for p in data.get("peluang", []):
                        st.write(f"**{p['kampus']}**")
                        st.progress(p["peluang"] / 100)
                        st.caption(f"📈 Peluang diterima: {p['peluang']}%")

                else:
                    st.error(data.get("message", "Gagal submit tryout."))
            except Exception:
                st.error("Tidak dapat terhubung ke server tryout.")

        if st.button("🔄 Ulang Tryout", key="ulang_tryout", type="primary"):
            st.session_state.tryout_started = False
            st.session_state.tryout_questions = []
            st.session_state.tryout_answers = []
            st.session_state.selected_kampus = []
            st.session_state.selected_jurusan = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ================= TES MINAT & BAKAT =================
    st.markdown("""
    <div class="panel-card">
        <div class="section-title">🧠 Tes Minat & Bakat</div>
        <div class="section-subtitle">
            Temukan jurusan yang paling cocok berdasarkan minat dan hobimu.
        </div>
    """, unsafe_allow_html=True)

    minat = st.multiselect(
        "🎯 Pilih Minat",
        [
            "Teknologi",
            "Bisnis",
            "Desain",
            "Kesehatan",
            "Psikologi",
            "Pendidikan",
            "Komunikasi",
            "Sains",
            "Game",
            "Matematika",
            "Sosial",
            "Hukum"
        ],
        placeholder="Pilih beberapa minat...",
        key="minat_assessment"
    )

    hobi = st.multiselect(
        "🎮 Pilih Hobi",
        [
            "Coding",
            "Game",
            "Menggambar",
            "Menulis",
            "Membaca",
            "Public Speaking",
            "Fotografi",
            "Editing Video",
            "Musik",
            "Olahraga",
            "Eksperimen",
            "Bisnis Online"
        ],
        placeholder="Pilih beberapa hobi...",
        key="hobi_assessment"
    )

    analisis = st.button("🔍 Analisis Minat Bakat", key="analisis_minat_btn", type="primary")

    if analisis:
        hasil = []

        if "Teknologi" in minat or "Coding" in hobi:
            hasil.append({
                "jurusan": "Sarjana Teknik Informatika",
                "persen": 92,
                "desc": "Cocok untuk kamu yang suka teknologi, logika, coding, dan pengembangan software.",
                "karier": ["Software Engineer", "Web Developer", "AI Engineer", "Cyber Security"]
            })

        if "Bisnis" in minat:
            hasil.append({
                "jurusan": "Sarjana Bisnis Digital",
                "persen": 87,
                "desc": "Cocok untuk kamu yang tertarik dunia bisnis modern dan startup digital.",
                "karier": ["Digital Marketer", "Business Analyst", "Entrepreneur", "Content Strategist"]
            })

        if "Game" in hobi:
            hasil.append({
                "jurusan": "Sarjana Game Development",
                "persen": 84,
                "desc": "Cocok untuk kamu yang suka dunia game, kreativitas, dan teknologi interaktif.",
                "karier": ["Game Developer", "Game Designer", "3D Artist", "Game Programmer"]
            })

        if "Desain" in minat or "Menggambar" in hobi:
            hasil.append({
                "jurusan": "Desain Komunikasi Visual",
                "persen": 80,
                "desc": "Cocok untuk kamu yang kreatif dan suka visual design.",
                "karier": ["Graphic Designer", "UI/UX Designer", "Illustrator", "Creative Director"]
            })

        if hasil:
            st.markdown("### 🎓 Rekomendasi Jurusan")
            for h in hasil:
                st.markdown(f"#### {h['jurusan']}")
                st.progress(h["persen"] / 100)
                st.caption(f"📈 Kecocokan: {h['persen']}%")
                st.info(h["desc"])

                st.markdown("**💼 Prospek Karier:**")
                for karier in h["karier"]:
                    st.write(f"✅ {karier}")

                st.markdown("---")
        else:
            st.warning("""
Belum ditemukan jurusan yang cocok.

Coba pilih minat dan hobi lebih banyak supaya sistem bisa menganalisis lebih akurat 🚀
            """)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# BACKEND CHAT PROCESS
# =========================================================
if st.session_state.is_loading:
    try:
        res = requests.post(
            f"{API_URL}/chat/rekomendasi",
            json={"pesan": messages[-1]["content"]}
        )
        data = res.json()

        if data.get("status") == "success":
            pesan = data.get("pesan", "")
            rekom = data.get("rekomendasi", [])
            response = f"{pesan}\n\n"

            for i, r in enumerate(rekom, 1):
                response += f"**{i}. {r['jurusan']}** — {r['persentase_cocok']}% cocok\n"
                response += f"{r['alasan']}\n\n"
                response += f"Prospek karir: {', '.join(r['prospek_karir'])}\n"
                response += f"Tips: {r['tips']}\n\n"
                response += "---\n"

        elif data.get("status") == "out_of_topic":
            response = data.get("pesan", "Pertanyaan di luar topik.")
        else:
            response = "Maaf, terjadi kesalahan. Coba lagi ya!"

    except Exception:
        response = "Tidak dapat terhubung ke server. Pastikan backend sudah berjalan."

    try:
        if st.session_state.last_user_message:
            requests.post(
                f"{API_URL}/chat/simpan",
                json={
                    "user_id": user_id,
                    "pesan_user": st.session_state.last_user_message,
                    "respons_ai": response
                }
            )
    except Exception as e:
        print("ERROR SIMPAN CHAT:", e)

    messages.append({"role": "assistant", "content": response})
    st.session_state.chat_history[st.session_state.current_chat] = messages
    st.session_state.is_loading = False
    st.rerun()