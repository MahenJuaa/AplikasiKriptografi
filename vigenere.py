import streamlit as st
import pandas as pd


def enkripsi_vigenere(plaintext, key):
    ciphertext = ""
    index_key = 0
    key = key.upper()

    for c in plaintext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            geser = ord(key[index_key % len(key)]) - ord('A')
            huruf_baru = chr((ord(c) - base + geser) % 26 + base)
            ciphertext += huruf_baru
            index_key += 1
        else:
            ciphertext += c

    return ciphertext


def dekripsi_vigenere(ciphertext, key):
    plaintext = ""
    index_key = 0
    key = key.upper()

    for c in ciphertext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            geser = ord(key[index_key % len(key)]) - ord('A')
            huruf_asli = chr((ord(c) - base - geser) % 26 + base)
            plaintext += huruf_asli
            index_key += 1
        else:
            plaintext += c

    return plaintext


def proses_vigenere(teks, key, mode="enkripsi"):
    """Menghasilkan detail proses per karakter untuk ditampilkan di tabel."""
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
                "Karakter": c,
                "Key": "-",
                "Nilai Karakter": "-",
                "Nilai Key": "-",
                "Rumus": "dilewati (bukan huruf)",
                "Hasil": c
            })
            hasil_akhir += c

    return hasil_akhir, hasil_proses


st.title("🔐 Vigenère Cipher")
st.write("Algoritma kriptografi klasik dengan substitusi polialfabetik")

with st.expander("📖 Lihat rumus & penjelasan"):
    st.latex(r"Enkripsi: C_i = (P_i + K_i) \mod 26")
    st.latex(r"Dekripsi: P_i = (C_i - K_i) \mod 26")
    st.write("Karakter non-huruf (spasi, tanda baca, angka) akan dilewati dan tidak ikut digeser.")

mode = st.radio("Pilih mode:", ["Enkripsi", "Dekripsi"], horizontal=True)

teks_input = st.text_area("Masukkan teks:", placeholder="Contoh: Hello, World!")
key_input = st.text_input("Masukkan key:", placeholder="Contoh: key")

if st.button("🔄 Proses"):
    if not teks_input or not key_input:
        st.warning("⚠️ Teks dan key tidak boleh kosong!")
    elif not key_input.isalpha():
        st.warning("⚠️ Key hanya boleh berisi huruf!")
    else:
        if mode == "Enkripsi":
            hasil_akhir, detail_proses = proses_vigenere(teks_input, key_input, mode="enkripsi")
        else:
            hasil_akhir, detail_proses = proses_vigenere(teks_input, key_input, mode="dekripsi")

        st.success(f"✅ Hasil {mode}:")
        st.code(hasil_akhir, language=None)

        st.subheader("📊 Detail Proses")
        df = pd.DataFrame(detail_proses)
        st.dataframe(df, use_container_width=True)