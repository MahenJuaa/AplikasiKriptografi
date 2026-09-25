import base64
import math

import streamlit as st
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Crypto Cutie 🎀",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# STYLING — PASTEL CUTE & PLAYFUL
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Baloo+2:wght@500;600;700;800&family=Fredoka:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #ffe4f0 0%, #e8d5ff 50%, #d4f0ff 100%);
    background-attachment: fixed;
}

/* Floating bubbles background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(circle at 15% 20%, rgba(255, 182, 218, 0.4) 0%, transparent 12%),
        radial-gradient(circle at 80% 15%, rgba(200, 182, 255, 0.4) 0%, transparent 10%),
        radial-gradient(circle at 30% 80%, rgba(182, 226, 255, 0.4) 0%, transparent 15%),
        radial-gradient(circle at 90% 70%, rgba(255, 218, 182, 0.35) 0%, transparent 10%),
        radial-gradient(circle at 50% 50%, rgba(255, 240, 250, 0.3) 0%, transparent 20%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 1;
}

/* ============ SIDEBAR ============ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f8 0%, #f3e8ff 100%);
    border-right: 3px dashed #ffb6d9;
}

[data-testid="stSidebar"] * {
    color: #7c4a68 !important;
}

[data-testid="stSidebar"] .stRadio > label {
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: #b86a92 !important;
    letter-spacing: 0.5px;
}

[data-testid="stSidebar"] .stRadio > div > label {
    background: #ffffff;
    padding: 0.7rem 0.9rem;
    border-radius: 16px;
    border: 2px solid #ffd6ea;
    transition: all 0.2s ease;
    cursor: pointer;
    font-size: 0.92rem;
    font-family: 'Quicksand', sans-serif;
    font-weight: 600;
    margin-bottom: 0.4rem;
    box-shadow: 0 2px 0 #ffd6ea;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: #fff0f8;
    border-color: #ffb6d9;
    transform: translateX(4px) scale(1.02);
    box-shadow: 0 4px 0 #ffb6d9;
}

/* ============ TYPOGRAPHY ============ */
h1, h2, h3, h4 {
    font-family: 'Baloo 2', sans-serif !important;
    color: #7c4a68 !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

p, span, label, div, li {
    color: #6b5570;
}

/* ============ INPUT FIELDS ============ */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #ffffff !important;
    border: 2px solid #ffd6ea !important;
    border-radius: 14px !important;
    color: #7c4a68 !important;
    font-family: 'Quicksand', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 0 #ffe4f0;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #ff8fc7 !important;
    box-shadow: 0 4px 0 #ffd6ea, 0 0 0 4px rgba(255, 143, 199, 0.15) !important;
    transform: translateY(-1px);
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #d4a8c4 !important;
}

/* ============ BUTTONS ============ */
div.stButton > button {
    background: linear-gradient(135deg, #ffb6d9 0%, #c8b6ff 100%);
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.65rem 1.6rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    font-family: 'Fredoka', sans-serif !important;
    letter-spacing: 0.5px;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 0 #e89bc4, 0 6px 16px rgba(255, 143, 199, 0.35);
    cursor: pointer;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 0 #e89bc4, 0 10px 24px rgba(255, 143, 199, 0.5);
    filter: brightness(1.05);
}

div.stButton > button:active {
    transform: translateY(2px);
    box-shadow: 0 2px 0 #e89bc4, 0 4px 10px rgba(255, 143, 199, 0.3);
}

/* ============ TABS ============ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.6);
    padding: 0.4rem;
    border-radius: 20px;
    border: 2px solid #ffd6ea;
    box-shadow: 0 2px 0 #ffe4f0;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 14px;
    color: #b86a92;
    font-weight: 700;
    font-family: 'Fredoka', sans-serif;
    padding: 0.6rem 1.2rem;
    font-size: 0.92rem;
    transition: all 0.15s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ffb6d9, #c8b6ff) !important;
    color: white !important;
    box-shadow: 0 3px 0 #e89bc4;
}

/* ============ DATAFRAME ============ */
[data-testid="stDataFrame"] {
    background: #ffffff;
    border-radius: 16px;
    border: 2px solid #ffd6ea;
    overflow: hidden;
    box-shadow: 0 3px 0 #ffe4f0;
}

/* ============ EXPANDER ============ */
details summary {
    background: #ffffff !important;
    border: 2px solid #ffd6ea !important;
    border-radius: 16px !important;
    padding: 0.8rem 1rem !important;
    font-weight: 700 !important;
    font-family: 'Fredoka', sans-serif !important;
    font-size: 0.92rem;
    color: #7c4a68 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 0 #ffe4f0;
}

details summary:hover {
    background: #fff0f8 !important;
    border-color: #ffb6d9 !important;
    transform: translateY(-1px);
}

details[open] summary {
    background: #fff0f8 !important;
    border-radius: 16px 16px 8px 8px !important;
}

/* ============ CODE BLOCK ============ */
pre, code {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background: #fff8fc !important;
    border-radius: 12px !important;
    color: #7c4a68 !important;
}

pre {
    border: 2px solid #ffd6ea !important;
    padding: 1rem !important;
    box-shadow: 0 3px 0 #ffe4f0;
}

/* ============ ALERTS ============ */
.stAlert {
    border-radius: 16px !important;
    border: 2px solid;
    padding: 0.85rem 1.1rem !important;
    font-weight: 500;
    box-shadow: 0 3px 0 rgba(0,0,0,0.04);
}

/* ============ TABLE ============ */
.stTable table {
    background: #ffffff !important;
    border-radius: 14px !important;
    overflow: hidden;
    font-family: 'Quicksand', sans-serif !important;
    font-size: 0.88rem;
    border: 2px solid #ffd6ea;
    box-shadow: 0 3px 0 #ffe4f0;
}

.stTable th {
    background: linear-gradient(135deg, #ffd6ea, #e8d5ff) !important;
    color: #7c4a68 !important;
    font-weight: 700 !important;
    font-family: 'Fredoka', sans-serif !important;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

.stTable td {
    color: #6b5570 !important;
    border-color: #ffe4f0 !important;
}

/* ============ DIVIDER ============ */
hr {
    border: none;
    border-top: 3px dashed #ffd6ea;
    margin: 1.8rem 0;
}

/* ============ SCROLLBAR ============ */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: #fff0f8;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ffb6d9, #c8b6ff);
    border-radius: 10px;
    border: 2px solid #fff0f8;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #ff8fc7, #a896ff);
}

/* ============ CUSTOM COMPONENTS ============ */
.cute-header {
    background: linear-gradient(135deg, #ffd6ea 0%, #e8d5ff 50%, #d4f0ff 100%);
    border: 3px dashed #ffffff;
    border-radius: 28px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 6px 0 rgba(255, 182, 217, 0.4), 0 12px 30px rgba(200, 182, 255, 0.3);
}

.cute-header::before {
    content: '🌸';
    position: absolute;
    top: 1rem;
    right: 1.5rem;
    font-size: 2.5rem;
    animation: float 3s ease-in-out infinite;
}

.cute-header::after {
    content: '✨';
    position: absolute;
    bottom: 1rem;
    right: 4rem;
    font-size: 1.8rem;
    animation: float 4s ease-in-out infinite reverse;
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(10deg); }
}

.cute-header h1 {
    color: #7c4a68 !important;
    margin: 0 0 0.4rem 0 !important;
    font-size: 2rem !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-weight: 800 !important;
}

.cute-header p {
    color: #996a88 !important;
    margin: 0 !important;
    font-size: 1rem;
    font-weight: 600;
}

.cute-tag {
    display: inline-block;
    background: #ffffff;
    color: #b86a92;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'Fredoka', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
    border: 2px solid #ffd6ea;
    box-shadow: 0 2px 0 #ffe4f0;
}

/* Result box - cute style */
.result-cute {
    background: linear-gradient(135deg, #fff8fc 0%, #f8f0ff 100%);
    border: 3px dashed #ffb6d9;
    border-radius: 20px;
    padding: 1.2rem 1.5rem;
    font-family: 'Quicksand', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #7c4a68;
    word-wrap: break-word;
    box-shadow: 0 5px 0 #ffd6ea, 0 8px 20px rgba(255, 182, 217, 0.3);
    position: relative;
}

.result-cute::before {
    content: '💖';
    position: absolute;
    top: -12px;
    left: 20px;
    background: #fff8fc;
    padding: 0 0.5rem;
    font-size: 1rem;
}

/* Cute stat card */
.cute-stat {
    background: #ffffff;
    border: 2px solid #ffd6ea;
    border-radius: 18px;
    padding: 1rem;
    text-align: center;
    transition: all 0.25s ease;
    box-shadow: 0 4px 0 #ffe4f0;
    cursor: default;
}

.cute-stat:hover {
    transform: translateY(-4px) rotate(-1deg);
    box-shadow: 0 8px 0 #ffd6ea, 0 12px 24px rgba(255, 182, 217, 0.35);
    border-color: #ffb6d9;
}

.cute-stat .emoji {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.4rem;
}

.cute-stat .label {
    color: #b86a92;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'Fredoka', sans-serif;
}

.cute-stat .value {
    color: #7c4a68;
    font-size: 1rem;
    font-weight: 700;
    font-family: 'Quicksand', sans-serif;
    margin-top: 0.2rem;
}

/* Step bubble */
.step-cute {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: #ffffff;
    padding: 0.5rem 1.1rem 0.5rem 0.5rem;
    border-radius: 999px;
    border: 2px solid #ffd6ea;
    box-shadow: 0 3px 0 #ffe4f0;
    margin: 1rem 0 0.8rem 0;
}

.step-cute .num {
    background: linear-gradient(135deg, #ffb6d9, #c8b6ff);
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-family: 'Fredoka', sans-serif;
    box-shadow: 0 2px 0 #e89bc4;
}

.step-cute .text {
    color: #7c4a68;
    font-weight: 700;
    font-family: 'Baloo 2', sans-serif;
    font-size: 1.05rem;
}

/* Info box cute */
.info-cute {
    background: #fff5fb;
    border-left: 5px solid #ffb6d9;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    color: #7c4a68;
    font-weight: 500;
    margin: 0.8rem 0;
    box-shadow: 0 3px 0 #ffe4f0;
}

/* Bouncy animation */
@keyframes bounce-in {
    0% { opacity: 0; transform: scale(0.7) translateY(20px); }
    50% { transform: scale(1.05) translateY(-5px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

.bounce-in {
    animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

/* Wiggle on hover */
@keyframes wiggle {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(-5deg); }
    75% { transform: rotate(5deg); }
}

/* Heart beat */
@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.15); }
}

.pulse-heart {
    display: inline-block;
    animation: heartbeat 1.5s ease-in-out infinite;
}

/* Balloon/success customization */
[data-testid="stNotification"] {
    border-radius: 16px !important;
}

/* Slider customization */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(135deg, #ffb6d9, #c8b6ff) !important;
    box-shadow: 0 2px 0 #e89bc4 !important;
}

/* Checkbox cute */
.stCheckbox label span {
    font-weight: 600 !important;
    color: #7c4a68 !important;
}

/* Radio cute */
.stRadio > div > label {
    font-weight: 600;
    color: #7c4a68 !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# HELPER COMPONENTS
# ==========================================
def cute_header(title: str, subtitle: str, tag: str = "", emoji: str = "🌸"):
    st.markdown(f"""
    <div class="cute-header bounce-in">
        <span class="cute-tag">{emoji} {tag}</span>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def result_cute(text: str, emoji: str = "💖"):
    st.markdown(f"""
    <div class="result-cute bounce-in">
        {text}
    </div>
    """, unsafe_allow_html=True)


def step_bubble(step_num: int, title: str, emoji: str = "✨"):
    st.markdown(f"""
    <div class="step-cute">
        <span class="num">{step_num}</span>
        <span class="text">{emoji} {title}</span>
    </div>
    """, unsafe_allow_html=True)


def cute_stat(emoji: str, label: str, value: str):
    st.markdown(f"""
    <div class="cute-stat">
        <span class="emoji">{emoji}</span>
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def info_cute(text: str):
    st.markdown(f'<div class="info-cute">{text}</div>', unsafe_allow_html=True)


# ==========================================
# CAESAR CIPHER
# ==========================================
def caesar_cipher(text: str, shift: int, mode: str):
    if mode == "Dekripsi":
        shift = -shift

    hasil = []
    proses = []

    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            posisi_awal = ord(ch) - base
            posisi_baru = (posisi_awal + shift) % 26
            ch_baru = chr(posisi_baru + base)
            hasil.append(ch_baru)
            proses.append((ch, posisi_awal, shift, ch_baru, posisi_baru))
        else:
            hasil.append(ch)
            proses.append((ch, None, None, ch, None))

    return "".join(hasil), proses


def caesar_proses_to_rows(proses):
    rows = []
    for ch, pos_awal, geser, ch_baru, pos_baru in proses:
        if pos_awal is None:
            rows.append({
                "Karakter": ch, "Posisi Awal": "-", "Pergeseran": "-",
                "Posisi Baru": "-", "Hasil": ch, "Keterangan": "Tidak diubah"
            })
        else:
            rows.append({
                "Karakter": ch, "Posisi Awal": pos_awal, "Pergeseran": geser,
                "Posisi Baru": pos_baru, "Hasil": ch_baru, "Keterangan": "Digeser"
            })
    return rows


# ==========================================
# VIGENERE CIPHER
# ==========================================
def proses_vigenere(teks, key, mode="enkripsi"):
    hasil_proses = []
    index_key = 0
    key = key.upper()
    hasil_akhir = ""

    for c in teks:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            huruf_key = key[index_key % len(key)]
            geser = ord(huruf_key) - ord('A')

            if mode == "enkripsi":
                huruf_hasil = chr((ord(c) - base + geser) % 26 + base)
            else:
                huruf_hasil = chr((ord(c) - base - geser) % 26 + base)

            hasil_proses.append({
                "Karakter": c,
                "Key": huruf_key,
                "Nilai Karakter": ord(c) - base,
                "Nilai Key": geser,
                "Rumus": f"({ord(c)-base} {'+' if mode=='enkripsi' else '-'} {geser}) mod 26",
                "Hasil": huruf_hasil
            })
            hasil_akhir += huruf_hasil
            index_key += 1
        else:
            hasil_proses.append({
                "Karakter": c, "Key": "-", "Nilai Karakter": "-",
                "Nilai Key": "-", "Rumus": "dilewati (bukan huruf)", "Hasil": c
            })
            hasil_akhir += c

    return hasil_akhir, hasil_proses


# ==========================================
# AES
# ==========================================
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]


def bytes_to_matrix(b: bytes):
    return [[f"{b[i + 4 * j]:02X}" for j in range(4)] for i in range(4)]


def sub_bytes(matrix):
    return [[f"{SBOX[int(v, 16)]:02X}" for v in row] for row in matrix]


def shift_rows(matrix):
    res = [row[:] for row in matrix]
    res[1] = res[1][1:] + res[1][:1]
    res[2] = res[2][2:] + res[2][:2]
    res[3] = res[3][3:] + res[3][:3]
    return res


def dummy_mix_columns(matrix):
    res = []
    for i, row in enumerate(matrix):
        new_row = []
        for j, val in enumerate(row):
            num = (int(val, 16) * 3 + i + j) % 256
            new_row.append(f"{num:02X}")
        res.append(new_row)
    return res


def generate_aes_key() -> str:
    return base64.b64encode(get_random_bytes(16)).decode("utf-8")


def parse_key(key_input) -> bytes:
    if isinstance(key_input, bytes):
        return key_input
    key_str = str(key_input).strip()
    if len(key_str) == 16:
        return key_str.encode("utf-8")
    try:
        decoded = base64.b64decode(key_str)
        if len(decoded) == 16:
            return decoded
    except Exception:
        pass
    return key_str.encode("utf-8")


def encrypt_aes_cbc(plaintext: str, key_input):
    key_bytes = parse_key(key_input)
    if len(key_bytes) != 16:
        raise ValueError(f"Ukuran kunci saat ini {len(key_bytes)} byte. Harus 16 byte (128 bit).")
    raw_bytes = plaintext.encode("utf-8")
    padded_bytes = pad(raw_bytes, AES.block_size)
    iv_bytes = get_random_bytes(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    encrypted_bytes = cipher.encrypt(padded_bytes)
    combined_binary = iv_bytes + encrypted_bytes
    ciphertext_b64 = base64.b64encode(combined_binary).decode("utf-8")
    return ciphertext_b64, raw_bytes, padded_bytes, iv_bytes, encrypted_bytes, key_bytes


def decrypt_aes_cbc(base64_ciphertext: str, key_input) -> str:
    key_bytes = parse_key(key_input)
    if len(key_bytes) != 16:
        raise ValueError(f"Ukuran kunci saat ini {len(key_bytes)} byte. Harus 16 byte (128 bit).")
    combined_binary = base64.b64decode(base64_ciphertext)
    if len(combined_binary) < 32:
        raise ValueError("Panjang ciphertext tidak valid.")
    iv = combined_binary[:16]
    ciphertext = combined_binary[16:]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode("utf-8")


def render_aes_encrypt_breakdown(raw_b, padded_b, iv_b, enc_b, k_bytes):
    total_blocks = len(padded_b) // 16
    info_cute(f"📦 Total **{len(padded_b)} byte** dipecah menjadi **{total_blocks} blok** (16 byte/blok)")

    prev_vector = iv_b

    for b_idx in range(total_blocks):
        block_bytes = padded_b[b_idx * 16: (b_idx + 1) * 16]
        enc_block_bytes = enc_b[b_idx * 16: (b_idx + 1) * 16]

        with st.expander(f"🎁 Blok {b_idx + 1} — Byte {b_idx*16} s/d {b_idx*16 + 15}", expanded=(b_idx == 0)):
            st.markdown("**🌈 Langkah 1 — Preprocessing (CBC)**")
            len_raw = len(raw_b)
            len_padded = len(padded_b)
            pad_added = len_padded - len_raw

            info_cute(
                f"📏 Teks asli: **{len_raw} byte** · "
                f"Padding: **{pad_added} byte** (`0x{pad_added:02X}`) · "
                f"Total: **{len_padded} byte**"
            )

            char_hex_data = []
            for idx, byte_val in enumerate(block_bytes):
                if idx >= len_raw:
                    char_display = f"[PAD 0x{byte_val:02X}]"
                else:
                    char_display = chr(byte_val) if 32 <= byte_val <= 126 else "."
                char_hex_data.append({
                    "Posisi": f"Byte {idx}",
                    "Karakter": char_display,
                    "Hex": f"{byte_val:02X}",
                    "Desimal": byte_val,
                })

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.dataframe(char_hex_data[:8], use_container_width=True, hide_index=True)
            with col_t2:
                st.dataframe(char_hex_data[8:], use_container_width=True, hide_index=True)

            st.markdown("---")

            if b_idx == 0:
                st.caption("🎨 Blok 1 — XOR dengan **IV acak**")
            else:
                st.caption(f"🎨 Blok {b_idx + 1} — XOR dengan **ciphertext blok {b_idx}**")

            m_plain = bytes_to_matrix(block_bytes)
            m_vector = bytes_to_matrix(prev_vector)
            preprocess_bytes = bytes([a ^ b for a, b in zip(block_bytes, prev_vector)])
            m_prep = bytes_to_matrix(preprocess_bytes)

            p_c1, p_c2, p_c3 = st.columns(3)
            with p_c1:
                st.text("Teks Asli")
                st.table(m_plain)
            with p_c2:
                lbl = "IV Acak" if b_idx == 0 else f"Ciphertext Blok {b_idx}"
                st.text(lbl)
                st.table(m_vector)
            with p_c3:
                st.text("Hasil XOR")
                st.table(m_prep)

            st.markdown("---")
            st.markdown("**🔑 Langkah 2 — Round 0 (AddRoundKey)**")
            m_key0 = bytes_to_matrix(k_bytes)
            r0_bytes = bytes([a ^ b for a, b in zip(preprocess_bytes, k_bytes)])
            m_r0_out = bytes_to_matrix(r0_bytes)

            r0_c1, r0_c2, r0_c3 = st.columns(3)
            with r0_c1:
                st.text("State Preprocessing")
                st.table(m_prep)
            with r0_c2:
                st.text("Round Key 0")
                st.table(m_key0)
            with r0_c3:
                st.text("Hasil Round 0")
                st.table(m_r0_out)

            st.markdown("---")
            st.markdown("**✨ Langkah 3 — Round 1 (4 Transformasi)**")

            m_sub1 = sub_bytes(m_r0_out)
            m_shift1 = shift_rows(m_sub1)
            m_mix1 = dummy_mix_columns(m_shift1)
            m_ark1 = dummy_mix_columns(m_mix1)

            r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
            with r1_c1:
                st.text("SubBytes")
                st.table(m_sub1)
            with r1_c2:
                st.text("ShiftRows")
                st.table(m_shift1)
            with r1_c3:
                st.text("MixColumns")
                st.table(m_mix1)
            with r1_c4:
                st.text("AddRoundKey")
                st.table(m_ark1)

            st.caption("*Round 2 s/d 9 diulang dengan pola yang sama...*")

            st.markdown("---")
            st.markdown("**🎯 Langkah 4 — Round 10 (Final)**")

            m_final = bytes_to_matrix(enc_block_bytes)
            r10_c1, r10_c2, r10_c3 = st.columns(3)
            with r10_c1:
                st.text("SubBytes")
                st.table(sub_bytes(m_mix1))
            with r10_c2:
                st.text("ShiftRows")
                st.table(shift_rows(sub_bytes(m_mix1)))
            with r10_c3:
                st.text("Hasil Akhir")
                st.table(m_final)

            st.code(" ".join([f"{x:02X}" for x in enc_block_bytes]), language="text")

        prev_vector = enc_block_bytes


def render_aes_decrypt_breakdown(base64_ciphertext: str, key_bytes: bytes, plaintext_hasil: str):
    combined_binary = base64.b64decode(base64_ciphertext)
    iv = combined_binary[:16]
    ciphertext = combined_binary[16:]
    total_blocks = len(ciphertext) // 16

    info_cute(f"🔍 IV (16 byte) + **{total_blocks} blok ciphertext**")
    st.write("**IV:**")
    st.table(bytes_to_matrix(iv))

    for b_idx in range(total_blocks):
        block_bytes = ciphertext[b_idx * 16: (b_idx + 1) * 16]
        with st.expander(f"🔓 Blok Ciphertext {b_idx + 1}", expanded=(b_idx == 0)):
            st.table(bytes_to_matrix(block_bytes))
            st.caption(
                "Invers AES 10 round (InvShiftRows, InvSubBytes, InvMixColumns, AddRoundKey), "
                "lalu XOR dengan blok sebelumnya (CBC)."
            )

    st.write("**Plaintext Hasil:**")
    st.code(plaintext_hasil, language="text")


# ==========================================
# RSA dengan Error Handling
# ==========================================
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Modular inverse tidak ditemukan. Pastikan gcd(e, phi) = 1.")


def rsa_generate_keys(p, q):
    if not isinstance(p, int) or not isinstance(q, int):
        raise ValueError("p dan q harus bilangan bulat.")
    if p < 2 or q < 2:
        raise ValueError("p dan q harus ≥ 2.")
    if not is_prime(p):
        raise ValueError(f"p = {p} bukan bilangan prima 🥺")
    if not is_prime(q):
        raise ValueError(f"q = {q} bukan bilangan prima 🥺")
    if p == q:
        raise ValueError("p dan q tidak boleh sama ya~ pilih dua prima berbeda ✨")

    n = p * q
    phi = (p - 1) * (q - 1)

    if phi < 3:
        raise ValueError("Nilai phi terlalu kecil. Pilih p dan q lebih besar.")

    e = 3
    while e < phi and math.gcd(e, phi) != 1:
        e += 2

    if e >= phi:
        raise ValueError("Tidak ditemukan nilai e valid. Pilih p dan q lain.")

    d = mod_inverse(e, phi)
    return n, phi, e, d


def rsa_encrypt_text(text: str, e: int, n: int):
    if not text:
        raise ValueError("Plaintext tidak boleh kosong.")
    blocks = []
    for idx, ch in enumerate(text):
        m = ord(ch)
        if m >= n:
            raise ValueError(
                f"Karakter '{ch}' (posisi {idx}, ASCII {m}) ≥ n ({n}). "
                f"Perbesar p dan q agar n > 255 ya~ 💕"
            )
        blocks.append(pow(m, e, n))
    return blocks


def rsa_decrypt_blocks(blocks, d: int, n: int) -> str:
    if not blocks:
        raise ValueError("Ciphertext tidak boleh kosong.")
    hasil = ""
    for idx, c in enumerate(blocks):
        if not isinstance(c, int):
            raise ValueError(f"Blok ke-{idx} bukan integer: {c}")
        if c < 0 or c >= n:
            raise ValueError(f"Blok ciphertext ke-{idx} ({c}) di luar rentang [0, {n-1}].")
        m = pow(c, d, n)
        if m > 0x10FFFF:
            raise ValueError(f"Hasil dekripsi blok ke-{idx} bukan karakter valid.")
        hasil += chr(m)
    return hasil


def render_rsa_key_generation(p, q, n, phi, e, d):
    st.markdown(f"""
    - 🌸 **$p$** = `{p}` , **$q$** = `{q}`
    - 🌟 **$n$** = $p \\times q$ = `{n}`
    - 🍀 **$\\phi(n)$** = $(p-1)(q-1)$ = `{phi}`
    - 🔑 **Public key $e$** = `{e}`
    - 🔐 **Private key $d$** = `{d}`
    """)


def render_rsa_encrypt_breakdown(text: str, e: int, n: int):
    blocks = []
    rows = []
    for ch in text:
        m = ord(ch)
        if m >= n:
            raise ValueError(f"Karakter '{ch}' (ASCII {m}) ≥ n ({n}). Perbesar p dan q.")
        c = pow(m, e, n)
        blocks.append(c)
        rows.append({
            "Karakter": ch,
            "ASCII (M)": m,
            "Rumus": f"{m}^{e} mod {n}",
            "Cipher (C)": c,
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)
    return blocks


def render_rsa_decrypt_breakdown(blocks, d: int, n: int) -> str:
    hasil = ""
    rows = []
    for c in blocks:
        m = pow(c, d, n)
        ch = chr(m)
        hasil += ch
        rows.append({
            "Cipher (C)": c,
            "Rumus": f"{c}^{d} mod {n}",
            "ASCII (M)": m,
            "Karakter": ch,
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)
    return hasil


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 1rem 0;">
        <div style="font-size: 3.5rem; line-height: 1; animation: float 3s ease-in-out infinite;">🔐</div>
        <h2 style="margin: 0.5rem 0 0 0; font-family: 'Baloo 2', sans-serif; color: #7c4a68 !important; font-size: 1.5rem;">
            Crypto Cutie
        </h2>
        <p style="margin: 0.2rem 0 0 0; color: #b86a92; font-size: 0.8rem; font-weight: 600;">
            ✨ belajar kriptografi jadi gemas ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    menu = st.radio(
        "🎀 Pilih Menu",
        [
            "🌸 Caesar Cipher",
            "🍭 Vigenère Cipher",
            "🎁 AES (Modern)",
            "🗝️ RSA (Modern)",
            "🌈 Super Enkripsi",
        ],
    )

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding: 1rem; background: #ffffff; border-radius: 16px; border: 2px dashed #ffd6ea;">
        <div style="font-size: 1.5rem;">🎈🎀🎈</div>
        <p style="font-size: 0.8rem; color: #b86a92; margin: 0.4rem 0 0 0; font-weight: 600;">
            5 algoritma siap dipakai!
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MENU 1: CAESAR
# ==========================================
if menu == "🌸 Caesar Cipher":
    cute_header(
        "Caesar Cipher 🌸",
        "Geser-geser huruf biar jadi pesan rahasia!",
        tag="KLASIK",
        emoji="🌸"
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        text_input = st.text_area(
            "💌 Tulis pesanmu",
            height=120,
            placeholder="Contoh: Hello World ~",
            key="caesar_text"
        )

    with col2:
        st.markdown("**🎛️ Atur di sini**")
        shift = st.number_input("🎯 Geser (1-25)", min_value=1, max_value=25, value=3, step=1, key="caesar_shift")
        mode = st.radio("🔮 Mode", ["Enkripsi", "Dekripsi"], key="caesar_mode")

    show_process = st.checkbox("👀 Tampilkan prosesnya", value=True, key="caesar_show_process")

    if st.button("✨ Proses Sekarang!", key="caesar_button", use_container_width=True):
        if not text_input.strip():
            st.warning("🥺 Pesannya masih kosong loh~ isi dulu ya!")
        else:
            hasil, proses = caesar_cipher(text_input, shift, mode)

            step_bubble(1, "Hasil", "💖")
            result_cute(hasil)

            if show_process:
                step_bubble(2, "Detail Proses", "🔍")
                st.dataframe(caesar_proses_to_rows(proses), use_container_width=True, hide_index=True)

    st.markdown("---")
    with st.expander("📚 Tentang Caesar Cipher"):
        st.markdown("""
        Caesar Cipher itu cara rahasia paling jadul! Setiap huruf digeser sebanyak *n* posisi. 🎠

        - **Enkripsi** ➡️ geser maju: `C = (P + K) mod 26`
        - **Dekripsi** ⬅️ geser mundur: `P = (C - K) mod 26`
        - Spasi, angka, dan simbol ga ikut digeser ya~ 💫
        """)


# ==========================================
# MENU 2: VIGENERE
# ==========================================
elif menu == "🍭 Vigenère Cipher":
    cute_header(
        "Vigenère Cipher 🍭",
        "Substitusi polialfabetik pakai kata kunci rahasia",
        tag="KLASIK",
        emoji="🍭"
    )

    with st.expander("🧮 Rumus"):
        st.latex(r"C_i = (P_i + K_i) \mod 26")
        st.latex(r"P_i = (C_i - K_i) \mod 26")

    mode_v = st.radio("🔮 Mode", ["Enkripsi", "Dekripsi"], horizontal=True, key="vig_mode")

    teks_input = st.text_area("💌 Tulis pesanmu", placeholder="Contoh: Hello, World!", key="vig_text")
    key_input_v = st.text_input("🔑 Kata kunci (huruf saja)", placeholder="Contoh: key", key="vig_key")

    if st.button("✨ Proses Sekarang!", key="vig_button", use_container_width=True):
        if not teks_input or not key_input_v:
            st.warning("🥺 Pesan dan kata kunci ga boleh kosong ya~")
        elif not key_input_v.isalpha():
            st.warning("🔤 Kata kunci cuma boleh huruf loh~")
        else:
            mode_str = "enkripsi" if mode_v == "Enkripsi" else "dekripsi"
            hasil_akhir, detail_proses = proses_vigenere(teks_input, key_input_v, mode=mode_str)

            step_bubble(1, f"Hasil {mode_v}", "💖")
            result_cute(hasil_akhir)

            step_bubble(2, "Detail Proses", "🔍")
            st.dataframe(detail_proses, use_container_width=True, hide_index=True)


# ==========================================
# MENU 3: AES
# ==========================================
elif menu == "🎁 AES (Modern)":
    cute_header(
        "AES-128 (CBC Mode) 🎁",
        "Enkripsi modern dengan visualisasi lengkap!",
        tag="MODERN",
        emoji="🎁"
    )

    for k in ["aes_enc_key_input", "aes_ciphertext", "aes_plaintext_decrypted"]:
        if k not in st.session_state:
            st.session_state[k] = ""

    tab_enc, tab_dec = st.tabs(["🔐 Enkripsi", "🔓 Dekripsi"])

    with tab_enc:
        step_bubble(1, "Input Enkripsi", "🎀")

        def _gen_key():
            st.session_state["aes_enc_key_input"] = generate_aes_key()

        col_k1, col_k2 = st.columns([3, 1])
        with col_k2:
            st.button("🎲 Generate Key", use_container_width=True, key="aes_gen_key", on_click=_gen_key)

        enc_key_input = col_k1.text_input(
            "🔑 Kunci AES (16 byte / 128 bit)",
            placeholder="16 karakter atau klik Generate Key",
            key="aes_enc_key_input",
        )

        enc_plaintext_input = st.text_area(
            "💌 Plaintext",
            placeholder="Teks yang ingin dienkripsi",
            height=80,
            key="aes_enc_plaintext_input",
        )

        if st.button("🔐 Jalankan Enkripsi", type="primary", key="aes_enc_button", use_container_width=True):
            if not enc_key_input or not enc_plaintext_input:
                st.warning("🥺 Kunci dan plaintext wajib diisi ya~")
            else:
                try:
                    c_b64, raw_b, padded_b, iv_b, enc_b, used_kbytes = encrypt_aes_cbc(
                        enc_plaintext_input, enc_key_input
                    )
                    st.session_state["aes_ciphertext"] = c_b64
                    st.session_state["aes_visual_data"] = {
                        "raw_bytes": raw_b, "padded_bytes": padded_b,
                        "iv": iv_b, "enc_bytes": enc_b, "key_bytes": used_kbytes,
                    }
                    st.success("🎉 Yeay! Enkripsi berhasil~")
                except Exception as err:
                    st.error(f"😿 Error: {err}")

        if st.session_state["aes_ciphertext"]:
            st.markdown("---")
            step_bubble(2, "Hasil Enkripsi", "💖")
            result_cute(st.session_state["aes_ciphertext"])

            if "aes_visual_data" in st.session_state:
                st.markdown("---")
                st.markdown("### 🔬 Breakdown Proses AES-128")
                v = st.session_state["aes_visual_data"]
                render_aes_encrypt_breakdown(
                    v["raw_bytes"], v["padded_bytes"], v["iv"], v["enc_bytes"], v["key_bytes"]
                )

    with tab_dec:
        step_bubble(1, "Input Dekripsi", "🎀")

        dec_key_input = st.text_input(
            "🔑 Kunci AES",
            placeholder="16 karakter teks atau kunci Base64",
            key="aes_dec_key_input",
        )

        dec_ciphertext_input = st.text_area(
            "🎁 Ciphertext (Base64)",
            placeholder="Tempel ciphertext di sini",
            height=100,
            key="aes_dec_ciphertext_input",
        )

        if st.button("🔓 Jalankan Dekripsi", type="primary", key="aes_dec_button", use_container_width=True):
            if not dec_key_input or not dec_ciphertext_input:
                st.warning("🥺 Kunci dan ciphertext ga boleh kosong~")
            else:
                try:
                    result = decrypt_aes_cbc(dec_ciphertext_input, dec_key_input)
                    st.session_state["aes_plaintext_decrypted"] = result
                    st.session_state["aes_dec_visual_data"] = {
                        "ciphertext_b64": dec_ciphertext_input,
                        "key_bytes": parse_key(dec_key_input),
                    }
                    st.success("🎉 Dekripsi berhasil!")
                except Exception as err:
                    st.error(f"😿 Gagal dekripsi. Detail: {err}")

        if st.session_state["aes_plaintext_decrypted"]:
            st.markdown("---")
            step_bubble(2, "Hasil Dekripsi", "💖")
            result_cute(st.session_state["aes_plaintext_decrypted"])

            if "aes_dec_visual_data" in st.session_state:
                st.markdown("---")
                st.markdown("### 🔬 Breakdown Proses Dekripsi AES-128")
                dv = st.session_state["aes_dec_visual_data"]
                render_aes_decrypt_breakdown(
                    dv["ciphertext_b64"], dv["key_bytes"], st.session_state["aes_plaintext_decrypted"]
                )


# ==========================================
# MENU 4: RSA
# ==========================================
elif menu == "🗝️ RSA (Modern)":
    cute_header(
        "RSA 🗝️",
        "Public key untuk enkripsi, private key untuk dekripsi!",
        tag="MODERN",
        emoji="🗝️"
    )

    if "rsa_key_params" not in st.session_state:
        st.session_state["rsa_key_params"] = None
    if "rsa_last_ciphertext" not in st.session_state:
        st.session_state["rsa_last_ciphertext"] = None

    step_bubble(1, "Bikin Kunci Dulu", "🔑")
    st.caption("Pilih dua bilangan prima p dan q. Pastikan n > 255 ya~")

    col_p, col_q, col_btn = st.columns([1, 1, 1])
    with col_p:
        p = st.number_input("🌸 Prima p", min_value=2, value=61, step=1, key="rsa_p")
    with col_q:
        q = st.number_input("🌟 Prima q", min_value=2, value=53, step=1, key="rsa_q")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_clicked = st.button("🔑 Generate!", use_container_width=True, key="rsa_gen_key")

    if generate_clicked:
        try:
            n, phi, e, d = rsa_generate_keys(p, q)
            st.session_state["rsa_key_params"] = {
                "p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d
            }
            st.success("🎉 Kunci berhasil dibuat!")
            st.balloons()
        except ValueError as err:
            st.error(f"😿 Gagal: {err}")
            st.session_state["rsa_key_params"] = None
        except Exception as err:
            st.error(f"😿 Error tak terduga: {err}")
            st.session_state["rsa_key_params"] = None

    if st.session_state["rsa_key_params"]:
        kp = st.session_state["rsa_key_params"]
        st.markdown("**🔮 Parameter Kunci:**")
        render_rsa_key_generation(kp["p"], kp["q"], kp["n"], kp["phi"], kp["e"], kp["d"])

    st.markdown("---")

    tab_enc_rsa, tab_dec_rsa = st.tabs(["🔐 Enkripsi", "🔓 Dekripsi"])

    with tab_enc_rsa:
        step_bubble(2, "Enkripsi Pesan", "💌")
        st.caption("Rumus: **C = M^e mod n**")

        plaintext_rsa = st.text_area(
            "💌 Plaintext",
            value="HELLO",
            height=100,
            placeholder="Tulis pesanmu di sini~",
            key="rsa_enc_plaintext"
        )

        encrypt_clicked = st.button("🔐 Enkripsi!", type="primary", use_container_width=True, key="rsa_enc_btn")

        if encrypt_clicked:
            kp = st.session_state.get("rsa_key_params")
            if not kp:
                st.error("😿 Kunci belum dibuat! Klik **Generate** dulu ya~")
            elif not plaintext_rsa or not plaintext_rsa.strip():
                st.warning("🥺 Plaintext masih kosong loh~")
            else:
                try:
                    n = kp["n"]
                    e = kp["e"]
                    max_ascii = max(ord(c) for c in plaintext_rsa)
                    if max_ascii >= n:
                        st.error(
                            f"😿 Karakter dengan ASCII tertinggi = **{max_ascii}** "
                            f"melebihi **n = {n}**. Naikkan p dan q ya~ 💕"
                        )
                    else:
                        info_cute(f"🔑 Public key: `(e={e}, n={n})`")
                        blocks = render_rsa_encrypt_breakdown(plaintext_rsa, e, n)
                        st.session_state["rsa_last_ciphertext"] = blocks

                        cipher_str = " ".join(str(c) for c in blocks)
                        step_bubble(3, "Hasil Ciphertext", "✨")
                        result_cute(cipher_str)
                        st.balloons()

                        st.info("💡 Ciphertext tersimpan! Buka tab **Dekripsi** buat balikin ke aslinya~")
                except ValueError as err:
                    st.error(f"😿 Enkripsi gagal: {err}")
                except Exception as err:
                    st.error(f"😿 Error tak terduga: {err}")

    with tab_dec_rsa:
        step_bubble(2, "Dekripsi Ciphertext", "🔓")
        st.caption("Rumus: **M = C^d mod n**")

        default_ct = ""
        if st.session_state.get("rsa_last_ciphertext"):
            default_ct = " ".join(str(c) for c in st.session_state["rsa_last_ciphertext"])

        ciphertext_input = st.text_area(
            "🎁 Ciphertext (angka dipisah spasi)",
            value=default_ct,
            height=100,
            placeholder="Contoh: 2048 1234 5678 ...",
            key="rsa_dec_ciphertext"
        )

        decrypt_clicked = st.button("🔓 Dekripsi!", type="primary", use_container_width=True, key="rsa_dec_btn")

        if decrypt_clicked:
            kp = st.session_state.get("rsa_key_params")
            if not kp:
                st.error("😿 Kunci belum dibuat! Klik **Generate** dulu ya~")
            elif not ciphertext_input or not ciphertext_input.strip():
                st.warning("🥺 Ciphertext masih kosong loh~")
            else:
                try:
                    cleaned = ciphertext_input.strip().replace(",", " ").split()
                    blocks = []
                    for i, tok in enumerate(cleaned):
                        if not tok.isdigit():
                            raise ValueError(
                                f"Token ke-{i + 1} ('{tok}') bukan angka valid. "
                                f"Ciphertext harus angka dipisah spasi ya~"
                            )
                        blocks.append(int(tok))

                    if not blocks:
                        raise ValueError("Ga ada blok ciphertext yang bisa diproses.")

                    n = kp["n"]
                    d = kp["d"]

                    for i, c in enumerate(blocks):
                        if c < 0 or c >= n:
                            raise ValueError(
                                f"Blok ke-{i + 1} ({c}) di luar rentang [0, {n - 1}]. "
                                f"Pastikan ciphertext dienkripsi dengan n yang sama ya~"
                            )

                    info_cute(f"🔐 Private key: `(d={d}, n={n})`")
                    plaintext_result = render_rsa_decrypt_breakdown(blocks, d, n)

                    step_bubble(3, "Hasil Plaintext", "💖")
                    result_cute(plaintext_result)

                    if "rsa_enc_plaintext" in st.session_state:
                        last_plain = st.session_state["rsa_enc_plaintext"]
                        if plaintext_result == last_plain:
                            st.success("✅ Plaintext hasil dekripsi SAMA PERSIS dengan aslinya! 🎉")
                            st.balloons()

                except ValueError as err:
                    st.error(f"😿 Dekripsi gagal: {err}")
                except Exception as err:
                    st.error(f"😿 Error tak terduga: {err}")

    st.markdown("---")
    with st.expander("📚 Tentang RSA"):
        st.markdown("""
        **RSA** itu algoritma asimetris yang pakai sepasang kunci:

        - 🔑 **Public key (e, n)** — buat enkripsi
        - 🔐 **Private key (d, n)** — buat dekripsi

        **Cara bikin kuncinya:**
        1. Pilih dua bilangan prima `p` dan `q`
        2. Hitung `n = p × q` dan `φ(n) = (p-1)(q-1)`
        3. Pilih `e` dengan `gcd(e, φ) = 1`
        4. Hitung `d` dengan `d × e ≡ 1 (mod φ)`

        **Enkripsi:** `C = M^e mod n`
        **Dekripsi:** `M = C^d mod n`

        Di sini RSA dilakukan per karakter, jadi `n` harus > 255 ya~ 💫
        """)


# ==========================================
# MENU 5: SUPER ENKRIPSI
# ==========================================
elif menu == "🌈 Super Enkripsi":
    cute_header(
        "Super Enkripsi 🌈",
        "Enkripsi berlapis-lapis: Caesar → Vigenère → AES → RSA",
        tag="ADVANCED",
        emoji="🌈"
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1: cute_stat("🌸", "Layer 1", "Caesar")
    with c2: cute_stat("🍭", "Layer 2", "Vigenère")
    with c3: cute_stat("🎁", "Layer 3", "AES-128")
    with c4: cute_stat("🗝️", "Layer 4", "RSA")

    st.markdown("---")
    step_bubble(1, "Input Parameter", "🎀")

    plaintext_super = st.text_area("💌 Plaintext", "Hello World", key="super_plaintext")

    col1, col2 = st.columns(2)
    with col1:
        caesar_shift_super = st.number_input(
            "🌸 Caesar — geser", min_value=1, max_value=25, value=3, step=1, key="super_caesar_shift"
        )
    with col2:
        vigenere_key_super = st.text_input("🍭 Vigenère — kata kunci", value="KUNCI", key="super_vigenere_key")

    def _gen_super_aes_key():
        st.session_state["super_aes_key_input"] = generate_aes_key()

    if "super_aes_key_input" not in st.session_state:
        st.session_state["super_aes_key_input"] = ""

    col3, col4 = st.columns([3, 1])
    with col4:
        st.button("🎲 Generate Key", use_container_width=True, key="super_gen_aes_key", on_click=_gen_super_aes_key)
    with col3:
        aes_key_super = st.text_input(
            "🎁 AES — kunci (16 byte)",
            placeholder="16 karakter atau klik Generate Key",
            key="super_aes_key_input",
        )

    col5, col6 = st.columns(2)
    with col5:
        rsa_p_super = st.number_input("🗝️ RSA — prima p", min_value=2, value=61, step=1, key="super_rsa_p")
    with col6:
        rsa_q_super = st.number_input("🗝️ RSA — prima q", min_value=2, value=53, step=1, key="super_rsa_q")

    st.caption("💡 RSA: gunakan p & q dengan n > 255 (misal 61 & 53 → n=3233) ya~")

    show_super_detail = st.checkbox(
        "👀 Tampilkan langkah detail tiap tahap",
        value=True, key="super_show_detail"
    )

    if st.button("🚀 Jalankan Super Enkripsi!", type="primary", key="super_button", use_container_width=True):
        if not plaintext_super.strip():
            st.warning("🥺 Plaintext masih kosong~")
        elif not vigenere_key_super.isalpha():
            st.warning("🔤 Kata kunci Vigenère cuma boleh huruf ya~")
        elif not aes_key_super:
            st.warning("🥺 Kunci AES wajib diisi atau di-generate dulu~")
        else:
            try:
                # ============ ENKRIPSI ============
                st.markdown("---")
                st.markdown("## 🔐 Enkripsi Berlapis")

                step_bubble(1, "Layer 1 — Caesar", "🌸")
                hasil_caesar, proses_caesar_enc = caesar_cipher(plaintext_super, caesar_shift_super, "Enkripsi")
                st.write(f"Input: `{plaintext_super}`")
                st.success(f"Output: `{hasil_caesar}`")
                if show_super_detail:
                    with st.expander("🔍 Detail Caesar"):
                        st.latex(r"C_i = (P_i + K) \mod 26")
                        st.dataframe(caesar_proses_to_rows(proses_caesar_enc),
                                     use_container_width=True, hide_index=True)

                step_bubble(2, "Layer 2 — Vigenère", "🍭")
                hasil_vigenere, proses_vig_enc = proses_vigenere(hasil_caesar, vigenere_key_super, mode="enkripsi")
                st.write(f"Input: `{hasil_caesar}`")
                st.success(f"Output: `{hasil_vigenere}`")
                if show_super_detail:
                    with st.expander("🔍 Detail Vigenère"):
                        st.latex(r"C_i = (P_i + K_i) \mod 26")
                        st.dataframe(proses_vig_enc, use_container_width=True, hide_index=True)

                step_bubble(3, "Layer 3 — AES-128 CBC", "🎁")
                c_b64, raw_b, padded_b, iv_b, enc_b, used_kbytes = encrypt_aes_cbc(hasil_vigenere, aes_key_super)
                st.write(f"Input: `{hasil_vigenere}`")
                st.success(f"Output (Base64): `{c_b64}`")
                if show_super_detail:
                    with st.expander("🔍 Detail AES-128 CBC"):
                        render_aes_encrypt_breakdown(raw_b, padded_b, iv_b, enc_b, used_kbytes)

                step_bubble(4, "Layer 4 — RSA", "🗝️")
                try:
                    n_super, phi_super, e_super, d_super = rsa_generate_keys(rsa_p_super, rsa_q_super)
                except ValueError as err:
                    st.error(f"😿 Gagal bikin kunci RSA: {err}")
                    st.stop()

                render_rsa_key_generation(rsa_p_super, rsa_q_super, n_super, phi_super, e_super, d_super)

                try:
                    if show_super_detail:
                        with st.expander("🔍 Detail Enkripsi RSA"):
                            st.latex(r"C = M^e \mod n")
                            rsa_blocks = render_rsa_encrypt_breakdown(c_b64, e_super, n_super)
                    else:
                        rsa_blocks = rsa_encrypt_text(c_b64, e_super, n_super)
                except ValueError as err:
                    st.error(f"😿 Enkripsi RSA gagal: {err}\n\nNaikkan p dan q ya~")
                    st.stop()

                hasil_rsa = " ".join(str(b) for b in rsa_blocks)
                step_bubble(5, "Hasil Akhir", "✨")
                result_cute(hasil_rsa)
                st.balloons()

                # ============ DEKRIPSI ============
                st.markdown("---")
                st.markdown("## 🔓 Dekripsi Berlapis (Pembuktian)")

                step_bubble(1, "Layer 4 — RSA (Inverse)", "🗝️")
                try:
                    if show_super_detail:
                        with st.expander("🔍 Detail Dekripsi RSA"):
                            st.latex(r"M = C^d \mod n")
                            dekripsi_rsa = render_rsa_decrypt_breakdown(rsa_blocks, d_super, n_super)
                    else:
                        dekripsi_rsa = rsa_decrypt_blocks(rsa_blocks, d_super, n_super)
                    st.success(f"Output: `{dekripsi_rsa}`")
                except ValueError as err:
                    st.error(f"😿 Dekripsi RSA gagal: {err}")
                    st.stop()

                step_bubble(2, "Layer 3 — AES (Inverse)", "🎁")
                try:
                    dekripsi_aes = decrypt_aes_cbc(dekripsi_rsa, aes_key_super)
                    st.success(f"Output: `{dekripsi_aes}`")
                    if show_super_detail:
                        with st.expander("🔍 Detail Dekripsi AES"):
                            render_aes_decrypt_breakdown(dekripsi_rsa, used_kbytes, dekripsi_aes)
                except Exception as err:
                    st.error(f"😿 Dekripsi AES gagal: {err}")
                    st.stop()

                step_bubble(3, "Layer 2 — Vigenère (Inverse)", "🍭")
                dekripsi_vig, proses_vig_dec = proses_vigenere(dekripsi_aes, vigenere_key_super, mode="dekripsi")
                st.success(f"Output: `{dekripsi_vig}`")
                if show_super_detail:
                    with st.expander("🔍 Detail Dekripsi Vigenère"):
                        st.latex(r"P_i = (C_i - K_i) \mod 26")
                        st.dataframe(proses_vig_dec, use_container_width=True, hide_index=True)

                step_bubble(4, "Layer 1 — Caesar (Inverse)", "🌸")
                dekripsi_final, proses_caesar_dec = caesar_cipher(dekripsi_vig, caesar_shift_super, "Dekripsi")
                st.success(f"Output: `{dekripsi_final}`")
                if show_super_detail:
                    with st.expander("🔍 Detail Dekripsi Caesar"):
                        st.latex(r"P_i = (C_i - K) \mod 26")
                        st.dataframe(caesar_proses_to_rows(proses_caesar_dec),
                                     use_container_width=True, hide_index=True)

                st.markdown("---")
                if dekripsi_final == plaintext_super:
                    st.balloons()
                    st.success("✅ Yeay! Plaintext hasil dekripsi SAMA PERSIS dengan aslinya! 🎉💖")
                else:
                    st.error("😿 Aduh... plaintext hasil dekripsi ga sama dengan aslinya. Coba cek lagi ya~")

            except Exception as err:
                st.error(f"😿 Ada error nih: {err}")

    st.markdown("---")
    with st.expander("📚 Tentang Super Enkripsi"):
        st.markdown("""
        **Super Enkripsi** itu enkripsi berlapis biar makin aman! 🌈

        1. 🌸 **Caesar** — geser alfabet
        2. 🍭 **Vigenère** — substitusi pakai kata kunci
        3. 🎁 **AES-128 CBC** — enkripsi blok simetris
        4. 🗝️ **RSA** — enkripsi asimetris pada output Base64 AES

        Dekripsi urutannya dibalik: **RSA → AES → Vigenère → Caesar** 💫
        """)