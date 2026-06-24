import streamlit as st
import requests

st.set_page_config(
    page_title="Login AI School Future",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/api"

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
    /* =========================
       FORCE LIGHT LOOK
       ========================= */
    :root {
        color-scheme: light !important;
    }

    html, body, [class*="css"] {
        color: #0f172a !important;
    }

    /* =========================
       HIDE SIDEBAR TOTAL
       ========================= */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="collapsedControl"] {
        display: none !important;
    }

    section[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* =========================
       GLOBAL APP BACKGROUND
       ========================= */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%) !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* =========================
       CARD
       ========================= */
    .auth-card {
        background: #ffffff !important;
        border-radius: 24px;
        padding: 36px 38px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.22);
        border: 1px solid #e5e7eb;
    }

    .auth-title {
        color: #0f172a !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 6px;
        line-height: 1.2;
    }

    .auth-subtitle {
        color: #475569 !important;
        font-size: 1rem;
        margin-bottom: 24px;
        line-height: 1.5;
    }

    .bottom-text {
        text-align: center;
        color: #ffffff !important;
        font-size: 15px;
        margin-top: 18px;
        margin-bottom: 10px;
        font-weight: 600;
    }

    /* =========================
       FORM WRAPPER
       ========================= */
    [data-testid="stForm"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* Label */
    [data-testid="stForm"] label,
    .stTextInput label,
    .stTextArea label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* =========================
       INPUT WRAPPER
       ========================= */
    div[data-baseweb="input"] > div {
        background-color: #f8fafc !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
        min-height: 48px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="input"] > div:hover {
        border-color: #94a3b8 !important;
    }

    div[data-baseweb="input"] > div:focus-within {
        border: 1.5px solid #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        background-color: #ffffff !important;
    }

    /* Input text */
    div[data-baseweb="input"] input {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        caret-color: #0f172a !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        background: transparent !important;
    }

    /* Placeholder */
    div[data-baseweb="input"] input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* Password eye icon */
    button[kind="secondary"] {
        color: #64748b !important;
    }

    /* Textarea kalau nanti dipakai */
    textarea {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        caret-color: #0f172a !important;
        background-color: #f8fafc !important;
        border-radius: 14px !important;
    }

    textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* =========================
       SUBMIT BUTTON
       ========================= */
    div.stFormSubmitButton > button {
        width: 100%;
        height: 50px;
        border-radius: 14px;
        border: none !important;
        font-weight: 800;
        font-size: 15px;
        color: #ffffff !important;
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%) !important;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28);
        transition: 0.2s ease;
    }

    div.stFormSubmitButton > button p,
    div.stFormSubmitButton > button span {
        color: #ffffff !important;
    }

    div.stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.05);
        box-shadow: 0 12px 26px rgba(37, 99, 235, 0.35);
    }

    /* =========================
       BUTTON PINDAH MODE
       Dibuat putih agar tidak nyaru
       ========================= */
    div.stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 14px;
        border: 1px solid #dbe2ea !important;
        background: #ffffff !important;
        color: #1e3a8a !important;
        font-weight: 800;
        font-size: 15px;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.10);
        transition: 0.2s ease;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: #1e3a8a !important;
    }

    div.stButton > button:hover {
        background: #eff6ff !important;
        border-color: #93c5fd !important;
        transform: translateY(-1px);
    }

    /* =========================
       ALERT
       ========================= */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid transparent !important;
        padding: 12px 14px !important;
    }

    [data-testid="stAlert"] * {
        color: inherit !important;
        font-weight: 600 !important;
    }

    /* SUCCESS */
    [data-testid="stAlert"][kind="success"] {
        background-color: #ecfdf5 !important;
        color: #065f46 !important;
        border-color: #a7f3d0 !important;
    }

    /* ERROR */
    [data-testid="stAlert"][kind="error"] {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border-color: #fecaca !important;
    }

    /* WARNING */
    [data-testid="stAlert"][kind="warning"] {
        background-color: #fffbeb !important;
        color: #92400e !important;
        border-color: #fde68a !important;
    }

    /* =========================
       EXTRA SPACING / TOOLBAR
       ========================= */
    [data-testid="stToolbar"] {
        right: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# 3. LAYOUT TENGAH
# =========================
left, center, right = st.columns([1.1, 3.8, 1.1])

with center:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    # =========================
    # 4. HALAMAN LOGIN
    # =========================
    if st.session_state.auth_mode == "login":
        st.markdown("<div class='auth-title'>Login AI</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Masuk ke akun AI School Future</div>",
            unsafe_allow_html=True
        )

        if st.session_state.register_success:
            st.success("Pendaftaran berhasil! Silakan login.")

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="example@mail.com")
            pwd   = st.text_input("Password", type="password", placeholder="******")

            submit = st.form_submit_button("LOG IN")

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
                        st.error(data.get("message", "Login gagal."))
                except Exception:
                    st.error("Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.")

    # =========================
    # 5. HALAMAN REGISTER
    # =========================
    else:
        st.markdown("<div class='auth-title'>Daftar Akun</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Lengkapi data diri kamu untuk membuat akun AI School Future</div>",
            unsafe_allow_html=True
        )

        with st.form("register_form"):
            nama      = st.text_input("Nama Lengkap", placeholder="Budi Santoso")
            email_reg = st.text_input("Email", placeholder="example@mail.com")
            pwd_reg   = st.text_input("Buat Password", type="password", placeholder="Min. 6 karakter")

            submit_reg = st.form_submit_button("BUAT AKUN")

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
                        st.error(data.get("message", "Registrasi gagal."))
                except Exception:
                    st.error("Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.")

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # 6. TOMBOL PINDAH MODE
    # =========================
    if st.session_state.auth_mode == "login":
        st.markdown("<div class='bottom-text'>Belum punya akun?</div>", unsafe_allow_html=True)
        if st.button("Ayo Daftar Sekarang", use_container_width=True, key="go_register"):
            switch_to_register()
            st.rerun()
    else:
        st.markdown("<div class='bottom-text'>Sudah punya akun?</div>", unsafe_allow_html=True)
        if st.button("Kembali ke Login", use_container_width=True, key="go_login"):
            switch_to_login()
            st.rerun()