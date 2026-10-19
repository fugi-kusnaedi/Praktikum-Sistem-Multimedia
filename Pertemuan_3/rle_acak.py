
# ==========================================
# IMPLEMENTASI RUN-LENGTH ENCODING (RLE)
# ==========================================

# Fungsi RLE Encoding
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


# Data acak
data_acak = "A7F2K9P3L8Q1"


# Proses Encoding
hasil_acak = rle_encode(data_acak)


# Menampilkan hasil
print("=== HASIL RUN-LENGTH ENCODING ===")
print("Data asli            :", data_acak)
print("Hasil RLE            :", hasil_acak)
print("Jumlah karakter      :", len(data_acak))
print("Jumlah pasangan RLE   :", len(hasil_acak))