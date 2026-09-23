import streamlit as st
import math

# Fungsi untuk mencari kunci privat (d)
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Mod inverse tidak ditemukan (p dan q mungkin tidak valid)")

# Konfigurasi Halaman
st.set_page_config(page_title="Aplikasi Kriptografi", page_icon="🔐", layout="wide")

# Sidebar Navigasi
st.sidebar.title("Navigasi Algoritma")
menu = st.sidebar.radio(
    "Pilih Menu:", 
    [
        "1. Caesar Cipher (Klasik)", 
        "2. Vigenère Cipher (Klasik)", 
        "3. AES (Modern)", 
        "4. RSA (Modern)", 
        "5. Super Enkripsi"
    ]
)

# ==========================================
# MENU 1 - 3: PLACEHOLDER UNTUK TEMANMU
# ==========================================
if menu == "1. Caesar Cipher (Klasik)":
    st.header("Caesar Cipher")
    st.info("Bagian ini akan dikerjakan oleh anggota kelompok lain.")

elif menu == "2. Vigenère Cipher (Klasik)":
    st.header("Vigenère Cipher")
    st.info("Bagian ini akan dikerjakan oleh anggota kelompok lain.")

elif menu == "3. AES (Modern)":
    st.header("AES (Advanced Encryption Standard)")
    st.info("Bagian ini akan dikerjakan oleh anggota kelompok lain.")

# ==========================================
# MENU 4: RSA (BAGIAN TUGASMU)
# ==========================================
elif menu == "4. RSA (Modern)":
    st.header("RSA (Rivest-Shamir-Adleman)")
    st.write("Algoritma asimetris yang menggunakan *Public Key* untuk enkripsi dan *Private Key* untuk dekripsi.")
    
    # Input dari User
    st.subheader("Input Parameter")
    col1, col2 = st.columns(2)
    with col1:
        p = st.number_input("Nilai Prima (p)", min_value=2, value=11, step=1)
    with col2:
        q = st.number_input("Nilai Prima (q)", min_value=2, value=13, step=1)
        
    pesan = st.text_area("Masukkan Plaintext:", "HELLO")
    
    if st.button("Jalankan Enkripsi RSA", type="primary"):
        try:
            # --- LOGIKA MATEMATIKA ---
            n = p * q
            phi = (p - 1) * (q - 1)
            
            e = 3
            while math.gcd(e, phi) != 1:
                e += 2
                
            d = mod_inverse(e, phi)
            
            # --- TAMPILAN PROSES KE LAYAR ---
            st.divider()
            st.subheader("1. Proses Pembangkitan Kunci")
            st.markdown(f"""
            * **Nilai $p$** = `{p}`, **Nilai $q$** = `{q}`
            * **Modulus ($n$)** = $p \\times q$ = `{n}`
            * **Euler Totient ($\\phi$)** = $(p-1) \\times (q-1)$ = `{phi}`
            * **Kunci Publik ($e$)** = `{e}` *(Syarat: FPB(e, $\\phi$) = 1)*
            * **Kunci Privat ($d$)** = `{d}` *(Syarat: $(d \\times e) \\pmod{{\\phi}} = 1$)*
            """)
            
            st.subheader("2. Proses Enkripsi ($C = M^e \\pmod n$)")
            
            ciphertext_blocks = []
            
            # Iterasi setiap karakter untuk ditampilkan prosesnya
            for char in pesan:
                m = ord(char) # Ubah ke ASCII
                c = pow(m, e, n) # Rumus Enkripsi RSA
                ciphertext_blocks.append(str(c))
                
                # Menampilkan breakdown per huruf
                st.write(f"Karakter **'{char}'** $\\rightarrow$ ASCII ($M$): **{m}** $\\rightarrow$ $({m}^{e}) \\pmod{{{n}}}$ = **{c}**")
            
            st.divider()
            st.success(f"**Hasil Ciphertext:** {' '.join(ciphertext_blocks)}")
            
        except Exception as err:
            st.error(f"Terjadi kesalahan perhitungan. Pastikan nilai p dan q adalah bilangan prima yang valid. Detail: {err}")

# ==========================================
# MENU 5: SUPER ENKRIPSI
# ==========================================
elif menu == "5. Super Enkripsi":
    st.header("Super Enkripsi")
    
    st.info("Bagian ini akan mengintegrasikan Caesar -> Vigenère -> AES -> RSA setelah semua algoritma selesai dibuat.")