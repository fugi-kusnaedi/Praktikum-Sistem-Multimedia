
# ==========================================
# IMPLEMENTASI RUN-LENGTH ENCODING (RLE)
# ==========================================

# Data asli
data = "AAAAAAABBBCC"
print("Data asli   :", data)


# Fungsi untuk melakukan RLE Encoding
def rle_encode(data):
    hasil = []

    if not data:
        return hasil

    jumlah = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            jumlah += 1
        else:
            hasil.append((data[i - 1], jumlah))
            jumlah = 1

    # Menyimpan karakter terakhir
    hasil.append((data[-1], jumlah))

    return hasil


# Proses Encoding
encoded = rle_encode(data)
print("Hasil encode:", encoded)


# Fungsi untuk melakukan RLE Decoding
def rle_decode(data):
    hasil = ""

    for simbol, jumlah in data:
        hasil += simbol * jumlah

    return hasil


# Proses Decoding
decoded = rle_decode(encoded)
print("Hasil decode:", decoded)


# Verifikasi hasil
print("\n--- Verifikasi RLE ---")
print("Data asli   :", data)
print("Hasil decode:", decoded)
print("Identik     :", data == decoded)