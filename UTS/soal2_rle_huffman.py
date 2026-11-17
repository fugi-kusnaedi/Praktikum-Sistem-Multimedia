# ==========================================
# SOAL 2 UTS - RLE & HUFFMAN UNTUK 'AAAABBBCCD'
# Mengadaptasi kode praktikum:
#   - Pertemuan_3/rle.py     (fungsi rle_encode / rle_decode)
#   - Pertemuan_3/hufman.py  (build_huffman_tree / build_codes / encode / decode)
# Menjalankan:  python3 soal2_rle_huffman.py
# ==========================================
import heapq
import itertools
import math
from collections import Counter

data = "AAAABBBCCD"
print("Data asli   :", data, f"({len(data)} karakter = {len(data) * 8} bit ASCII)")


# ==========================================
# (a) RUN-LENGTH ENCODING  (dari Pertemuan_3/rle.py)
# ==========================================
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


hasil_rle = rle_encode(data)
teks_rle = "".join(f"{jumlah}{simbol}" for simbol, jumlah in hasil_rle)

print("\n--- (a) Run-Length Encoding ---")
print("Hasil encode     :", hasil_rle)
print("Bentuk teks      :", teks_rle, f"({len(teks_rle)} karakter)")
print(f"Rasio RLE        : {len(data)}:{len(teks_rle)} = {len(data) / len(teks_rle):.2f} : 1")


# ==========================================
# (b) HUFFMAN  (dari Pertemuan_3/hufman.py)
# ==========================================
def build_huffman_tree(data):
    frekuensi = Counter(data)

    urutan = itertools.count()
    # Node = (frekuensi, no_urut, pohon). no_urut mencegah Python membandingkan
    # dua pohon saat frekuensi sama (kasus B=3 vs gabungan C+D=3) -> TypeError
    heap = [
        (jumlah, next(urutan), [jumlah, simbol])
        for simbol, jumlah in sorted(frekuensi.items())
    ]
    heapq.heapify(heap)

    while len(heap) > 1:
        kiri = heapq.heappop(heap)
        kanan = heapq.heappop(heap)

        gabungan = [
            kiri[0] + kanan[0],
            kiri[2],
            kanan[2]
        ]

        heapq.heappush(heap, (gabungan[0], next(urutan), gabungan))

    return heap[0][2]


def build_codes(tree, kode="", codes=None):
    if codes is None:
        codes = {}

    # Jika node merupakan daun, simpan kode simbol
    if len(tree) == 2:
        codes[tree[1]] = kode or "0"
        return codes

    build_codes(tree[1], kode + "0", codes)
    build_codes(tree[2], kode + "1", codes)

    return codes


def encode(data, codes):
    return "".join(codes[karakter] for karakter in data)


def decode(encoded, tree):
    hasil = []
    node = tree

    for bit in encoded:
        node = node[1] if bit == "0" else node[2]

        if len(node) == 2:
            hasil.append(node[1])
            node = tree

    return "".join(hasil)


frekuensi = Counter(data)
pohon = build_huffman_tree(data)
kode = build_codes(pohon)
encoded = encode(data, kode)
decoded = decode(encoded, pohon)

total_bit_huffman = sum(frekuensi[s] * len(k) for s, k in kode.items())
rata_rata = total_bit_huffman / len(data)
entropi = -sum((f / len(data)) * math.log2(f / len(data)) for f in frekuensi.values())

print("\n--- (b) Kode Huffman ---")
print("Frekuensi :", dict(frekuensi))
print("Simbol  Frekuensi  Kode    Panjang  Total bit")
for s in sorted(kode, key=lambda x: (-frekuensi[x], x)):
    print(f"  {s}        {frekuensi[s]}        {kode[s]:<7} {len(kode[s])}        {frekuensi[s] * len(kode[s])}")
print("Hasil encode :", encoded)
print("Hasil decode :", decoded)
print("Identik      :", data == decoded)
print(f"Total bit Huffman       = {total_bit_huffman} bit")
print(f"Rata-rata panjang kode  = {total_bit_huffman}/{len(data)} = {rata_rata:.2f} bit/simbol")
print(f"Entropi sumber H        = {entropi:.4f} bit/simbol (efisiensi = {entropi / rata_rata * 100:.1f}%)")


# ==========================================
# (c) PERBANDINGAN RASIO KOMPRESI
# ==========================================
bit_asli = len(data) * 8                 # ASCII 8 bit/karakter
bit_rle = len(teks_rle) * 8              # hasil RLE disimpan sebagai teks ASCII

print("\n--- (c) Perbandingan Rasio Kompresi ---")
print(f"ASCII asli  : {bit_asli} bit")
print(f"RLE         : {bit_rle} bit  -> rasio {bit_asli / bit_rle:.2f} : 1")
print(f"Huffman     : {total_bit_huffman} bit -> rasio {bit_asli / total_bit_huffman:.2f} : 1")
print("Kesimpulan  : Huffman lebih efektif karena mengeksploitasi distribusi")
print("              frekuensi simbol, bukan hanya panjang run yang pendek-pendek.")
