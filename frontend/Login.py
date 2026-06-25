import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Login AI School Future",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_URL}/api"

# =========================
# 1. SESSION STATE
# =========================
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if "user" not in st.session_state:
    st.session_state.user = None

if "register_success" not in st.session_state:
    st.session_state.register_success = False


def switch_to_register():
    st.session_state.auth_mode = "register"
    st.session_state.register_success = False


def switch_to_login():
    st.session_state.auth_mode = "login"


# =========================
# 2. CSS / STYLE
# =========================
st.markdown("""
<style>
    /* Force light color scheme agar tidak ada elemen gelap dari browser */
    :root {
        color-scheme: light !important;
    }

    html, body, [class*="css"] {
        color: #0f172a !important;
    }

    /* Sembunyikan sidebar */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%) !important;
        min-height: 100dvh !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Main container */
    .block-container {
        max-width: 1200px !important;
        padding-top: 4rem !important;
        padding-bottom: 3rem !important;
        padding-left: clamp(0.75rem, 4vw, 3rem) !important;
        padding-right: clamp(0.75rem, 4vw, 3rem) !important;
    }

    /* Wrapper card */
    .auth-wrapper {
        width: 100%;
        max-width: 480px;
        margin: 0 auto;
        padding: 0 0.5rem;
        box-sizing: border-box;
    }

    /* Card glassmorphism */
    .auth-card {
        background: rgba(255, 255, 255, 0.10) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 28px;
        padding: clamp(28px, 5vw, 40px) clamp(22px, 5vw, 36px);
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
        box-sizing: border-box;
        width: 100%;
    }

    /* Logo / brand icon */
    .auth-logo {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 18px;
        font-size: 24px;
    }

    .auth-title {
        color: #ffffff !important;
        font-size: clamp(1.8rem, 5vw, 2.2rem);
        font-weight: 800;
        margin: 0 0 6px 0 !important;
        line-height: 1.2;
        letter-spacing: -0.5px;
    }

    .auth-subtitle {
        color: #93c5fd !important;
        font-size: clamp(0.88rem, 2.5vw, 0.97rem);
        margin-bottom: 26px;
        line-height: 1.55;
    }

    .bottom-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.75) !important;
        font-size: clamp(13px, 3vw, 14px);
        margin-top: 16px;
        margin-bottom: 8px;
        font-weight: 500;
    }

    /* Divider tipis */
    .auth-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.12);
        margin: 20px 0;
    }

    /* ================================
       FORM — hilangkan background form
    ================================ */
    [data-testid="stForm"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* Label input */
    [data-testid="stForm"] label,
    .stTextInput label,
    .stTextArea label {
        color: rgba(255, 255, 255, 0.90) !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.2px;
    }

    /* ================================
       INPUT WRAPPER — fix hitam di kanan
       Paksa semua child div juga putih
    ================================ */
    div[data-baseweb="input"] {
        background: transparent !important;
    }

    div[data-baseweb="input"] > div {
        background: rgba(255, 255, 255, 0.97) !important;
        border: 1.5px solid transparent !important;
        border-radius: 14px !important;
        min-height: 52px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.12) !important;
        transition: all 0.2s ease !important;
        overflow: hidden !important;
    }

    /* Paksa SEMUA div child dalam input (termasuk slot eye icon) putih */
    div[data-baseweb="input"] > div > div,
    div[data-baseweb="input"] > div > div > div {
        background: rgba(255, 255, 255, 0.97) !important;
        color: #0f172a !important;
    }

    div[data-baseweb="input"] > div:hover {
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.16) !important;
        transform: translateY(-1px);
    }

    div[data-baseweb="input"] > div:focus-within {
        border: 1.5px solid #60a5fa !important;
        box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.20) !important;
        background: #ffffff !important;
        transform: translateY(-1px);
    }

    div[data-baseweb="input"] > div:focus-within > div,
    div[data-baseweb="input"] > div:focus-within > div > div {
        background: #ffffff !important;
    }

    /* Teks input */
    div[data-baseweb="input"] input {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        caret-color: #1d4ed8 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        background: transparent !important;
    }

    /* Placeholder */
    div[data-baseweb="input"] input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }

    /* ================================
       EYE ICON (tombol show/hide pw)
       Fix background hitam di sisi kanan
    ================================ */
    div[data-baseweb="input"] button,
    div[data-baseweb="input"] [role="button"] {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #64748b !important;
        cursor: pointer;
    }

    div[data-baseweb="input"] button:hover,
    div[data-baseweb="input"] [role="button"]:hover {
        background: transparent !important;
        background-color: rgba(241, 245, 249, 0.6) !important;
        color: #334155 !important;
    }

    div[data-baseweb="input"] button svg,
    div[data-baseweb="input"] [role="button"] svg {
        fill: #64748b !important;
        color: #64748b !important;
    }

    /* Selector fallback untuk berbagai versi Streamlit */
    button[kind="secondary"] {
        color: #64748b !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
    }

    /* ================================
       TEXTAREA
    ================================ */
    textarea {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        caret-color: #1d4ed8 !important;
        background-color: rgba(255, 255, 255, 0.97) !important;
        border-radius: 14px !important;
        font-size: 15px !important;
    }

    textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* ================================
       TOMBOL SUBMIT (dalam form)
    ================================ */
    div.stFormSubmitButton > button {
        width: 100%;
        height: 52px;
        border-radius: 14px;
        border: none !important;
        font-weight: 700;
        font-size: 15px;
        color: #ffffff !important;
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%) !important;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease;
        margin-top: 14px;
        letter-spacing: 0.3px;
    }

    div.stFormSubmitButton > button p,
    div.stFormSubmitButton > button span {
        color: #ffffff !important;
    }

    div.stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.08);
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.45) !important;
    }

    div.stFormSubmitButton > button:active {
        transform: translateY(0px);
    }

    /* ================================
       TOMBOL PINDAH MODE (di luar form)
    ================================ */
    div.stButton > button {
        width: 100%;
        height: 50px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.20) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(8px);
        color: #ffffff !important;
        font-weight: 600;
        font-size: 14px;
        box-shadow: none !important;
        transition: all 0.2s ease;
        letter-spacing: 0.2px;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: #ffffff !important;
    }

    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.35) !important;
        transform: translateY(-1px);
    }

    /* ================================
       ALERT / NOTIFIKASI
    ================================ */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid transparent !important;
        padding: 11px 14px !important;
        margin-bottom: 14px !important;
    }

    [data-testid="stAlert"] * {
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"],
    div[role="alert"].st-emotion-cache-j7qwjs {
        background-color: #ecfdf5 !important;
        color: #065f46 !important;
        border-color: #a7f3d0 !important;
    }

    div[data-testid="stAlert"][data-baseweb="notification"][kind="negative"] {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border-color: #fecaca !important;
    }

    div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
        background-color: #fffbeb !important;
        color: #92400e !important;
        border-color: #fde68a !important;
    }

    /* ================================
       MISC
    ================================ */
    [data-testid="stToolbar"] {
        right: 1rem;
    }

    .element-container {
        margin-bottom: 0.6rem !important;
    }

    /* ================================
       RESPONSIVE — MOBILE (≤ 640px)
    ================================ */
    @media screen and (max-width: 640px) {
        /* Sembunyikan kolom kiri & kanan, tengah jadi full width */
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
            display: none !important;
            flex: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }

        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) {
            flex: 1 1 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }

        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .auth-card {
            border-radius: 22px;
            padding: 26px 18px 22px 18px;
        }

        .auth-title {
            font-size: 1.7rem;
        }

        .auth-wrapper {
            padding: 0;
        }
    }

    /* ================================
       RESPONSIVE — TABLET (641px – 900px)
    ================================ */
    @media screen and (min-width: 641px) and (max-width: 900px) {
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
            flex: 0.4 !important;
            min-width: 0 !important;
        }

        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) {
            flex: 5 !important;
        }

        .block-container {
            padding-top: 3rem !important;
        }
    }

    /* ================================
       RESPONSIVE — DESKTOP (> 900px)
    ================================ */
    @media screen and (min-width: 901px) {
        .block-container {
            padding-top: 5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# =========================
# 3. LAYOUT TENGAH
# =========================
left, center, right = st.columns([1.1, 3.8, 1.1])

with center:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)

    # ── Logo kecil di atas card ──
    st.markdown("""
        <div style='text-align:center; margin-bottom: 10px;'>
            <div class='auth-logo' style='margin: 0 auto;'>🎓</div>
            <div style='color: rgba(255,255,255,0.55); font-size: 12px; font-weight: 600;
                        letter-spacing: 2px; text-transform: uppercase; margin-top: 4px;'>
                AI School Future
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    # =========================
    # 4. HALAMAN LOGIN
    # =========================
    if st.session_state.auth_mode == "login":
        st.markdown("<div class='auth-title'>Selamat Datang</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Masuk ke akun AI School Future kamu</div>",
            unsafe_allow_html=True
        )

        if st.session_state.register_success:
            st.success("✅ Pendaftaran berhasil! Silakan login.")

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="example@mail.com")
            pwd = st.text_input("Password", type="password", placeholder="Masukkan password")
            submit = st.form_submit_button("🔐  Masuk Sekarang")

        if submit:
            if not email or not pwd:
                st.error("Email dan password tidak boleh kosong!")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/login",
                        json={"email": email, "password": pwd}
                    )
                    data = res.json()

                    if data.get("status") == "success":
                        st.session_state.user = data["data"]
                        st.success(data.get("message", "Login berhasil!"))
                        st.switch_page("pages/Dashboard.py")
                    else:
                        st.error(data.get("message", "Email atau password salah."))
                except Exception:
                    st.error("⚠️ Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.")

    # =========================
    # 5. HALAMAN REGISTER
    # =========================
    else:
        st.markdown("<div class='auth-title'>Buat Akun</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Lengkapi data diri untuk mulai belajar bersama AI</div>",
            unsafe_allow_html=True
        )

        with st.form("register_form"):
            nama = st.text_input("Nama Lengkap", placeholder="Budi Santoso")
            email_reg = st.text_input("Email", placeholder="example@mail.com")
            pwd_reg = st.text_input("Buat Password", type="password", placeholder="Min. 6 karakter")
            submit_reg = st.form_submit_button("🚀  Buat Akun Sekarang")

        if submit_reg:
            if not nama or not email_reg or not pwd_reg:
                st.error("Semua kolom wajib diisi!")
            elif len(pwd_reg) < 6:
                st.error("Password minimal 6 karakter!")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/register",
                        json={
                            "nama_lengkap": nama,
                            "email": email_reg,
                            "password": pwd_reg
                        }
                    )
                    data = res.json()

                    if data.get("status") == "success":
                        st.session_state.register_success = True
                        switch_to_login()
                        st.rerun()
                    else:
                        st.error(data.get("message", "Registrasi gagal. Coba lagi."))
                except Exception:
                    st.error("⚠️ Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.")

    st.markdown("</div>", unsafe_allow_html=True)  # tutup auth-card

    # =========================
    # 6. TOMBOL PINDAH MODE
    # =========================
    if st.session_state.auth_mode == "login":
        st.markdown(
            "<div class='bottom-text'>Belum punya akun?</div>",
            unsafe_allow_html=True
        )
        if st.button("Daftar Sekarang →", use_container_width=True, key="go_register"):
            switch_to_register()
            st.rerun()
    else:
        st.markdown(
            "<div class='bottom-text'>Sudah punya akun?</div>",
            unsafe_allow_html=True
        )
        if st.button("← Kembali ke Login", use_container_width=True, key="go_login"):
            switch_to_login()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # tutup auth-wrapper