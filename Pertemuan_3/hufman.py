

# Implementasi Algoritma Huffman
from collections import Counter
import heapq


# 1. Membangun Huffman Tree
def build_huffman_tree(data):
    frekuensi = Counter(data)

    heap = [[jumlah, simbol] for simbol, jumlah in frekuensi.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        kiri = heapq.heappop(heap)
        kanan = heapq.heappop(heap)

        gabungan = [
            kiri[0] + kanan[0],
            kiri,
            kanan
        ]

        heapq.heappush(heap, gabungan)

    return heap[0]


# 2. Membuat Kode Huffman
def build_codes(tree, kode="", codes=None):
    if codes is None:
        codes = {}

    # Jika node merupakan daun, simpan kode simbol
    if len(tree) == 2:
        simbol = tree[1]
        codes[simbol] = kode or "0"
        return codes

    build_codes(tree[1], kode + "0", codes)
    build_codes(tree[2], kode + "1", codes)

    return codes


# 3. Proses Encoding
def encode(data, codes):
    return "".join(codes[karakter] for karakter in data)


# 4. Proses Decoding
def decode(encoded, tree):
    hasil = []
    node = tree

    for bit in encoded:
        node = node[1] if bit == "0" else node[2]

        # Jika mencapai daun, ambil simbol
        if len(node) == 2:
            hasil.append(node[1])
            node = tree

    return "".join(hasil)


# 5. Program Utama
data = "AAAAABBBC"

# Membangun pohon dan kode Huffman
tree = build_huffman_tree(data)
codes = build_codes(tree)

# Encoding dan decoding
encoded = encode(data, codes)
decoded = decode(encoded, tree)

# 6. Menampilkan Hasil
print("=== HASIL KOMPRESI HUFFMAN ===")
print("Data asli    :", data)
print("Frekuensi    :", dict(Counter(data)))
print("Kode Huffman :", codes)
print("Hasil encode :", encoded)
print("Hasil decode :", decoded)
print("Identik      :", data == decoded)