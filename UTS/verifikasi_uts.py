#!/usr/bin/env python3
# verifikasi_uts.py
# Verifikasi perhitungan kuantitatif untuk UTS Praktikum Sistem Multimedia (IFRWP5149)
# Menjalankan:  python3 verifikasi_uts.py

import heapq
import itertools
import math
from collections import Counter

GARIS = "=" * 64


def soal_1():
    print(GARIS)
    print("SOAL 1 - Ukuran file audio PCM mono, 5 s, 44.100 Hz, 16-bit")
    print(GARIS)
    sr, dur, bits, ch = 44100, 5, 16, 1
    sampel = sr * dur
    total_bit = sampel * bits * ch
    total_byte = total_bit // 8
    print("Rumus  : Ukuran = sample_rate x durasi x bit_depth x jumlah_kanal")
    print(f"Jumlah sampel = {sr} x {dur} s              = {sampel:,} sampel")
    print(f"Total bit     = {sampel:,} x {bits} bit x {ch} kanal = {total_bit:,} bit")
    print(f"Ukuran file   = {total_bit:,} / 8            = {total_byte:,} byte (~{total_byte / 1024:.1f} KiB)")
    print()


def soal_2():
    print(GARIS)
    print("SOAL 2 - RLE, Huffman, dan rasio kompresi untuk 'AAAABBBCCD'")
    print(GARIS)
    data = "AAAABBBCCD"
    n = len(data)

    # ---------- (a) Run-Length Encoding ----------
    rle, i = "", 0
    while i < n:
        j = i
        while j < n and data[j] == data[i]:
            j += 1
        rle += f"{j - i}{data[i]}"
        i = j
    print(f"Data asli  : {data}  ({n} karakter = {n * 8} bit)")
    print(f"Hasil RLE  : {rle}  ({len(rle)} karakter = {len(rle) * 8} bit)")
    print(f"Rasio RLE  : {n * 8}/{len(rle) * 8} = {n / len(rle):.2f} : 1")

    # ---------- (b) Huffman ----------
    freq = Counter(data)
    cnt = itertools.count()
    heap = [(f, next(cnt), {s: ""}) for s, f in sorted(freq.items())]
    heapq.heapify(heap)   # penting: list awal belum memenuhi invarian min-heap
    while len(heap) > 1:
        f1, _, m1 = heapq.heappop(heap)
        f2, _, m2 = heapq.heappop(heap)
        m = {s: "0" + c for s, c in m1.items()}
        m.update({s: "1" + c for s, c in m2.items()})
        heapq.heappush(heap, (f1 + f2, next(cnt), m))
    codes = heap[0][2]

    print("\nSimbol  Frekuensi  Kode    Panjang  Total bit")
    for s in sorted(freq, key=freq.get, reverse=True):
        print(f"  {s}        {freq[s]}        {codes[s]:<7} {len(codes[s])}        {freq[s] * len(codes[s])}")

    total_bit_huff = sum(freq[s] * len(codes[s]) for s in freq)
    avg = total_bit_huff / n
    H = -sum((f / n) * math.log2(f / n) for f in freq.values())
    print(f"\nRata-rata panjang kode = {total_bit_huff}/{n} = {avg:.2f} bit/simbol")
    print(f"Entropi sumber H       = {H:.4f} bit/simbol (efisiensi kode = {H / avg * 100:.1f}%)")
    print(f"Total bit Huffman      = {total_bit_huff} bit")
    print(f"Rasio Huffman          = {n * 8}/{total_bit_huff} = {n * 8 / total_bit_huff:.2f} : 1")
    print("Catatan: menukar kode C/D antar-cabang tetap valid, total bit tidak berubah.")
    print()


def soal_3():
    print(GARIS)
    print("SOAL 3 - Estimasi ukuran file podcast 60 menit")
    print(GARIS)
    dur = 60 * 60          # detik
    wav = 44100 * dur * 2 * 2          # 16 bit = 2 byte, stereo (2 kanal)
    aac128 = 128_000 * dur // 8
    aac96 = 96_000 * dur // 8
    mp3192 = 192_000 * dur // 8
    print(f"WAV 44,1 kHz / 16-bit / stereo : {wav:,} byte (~{wav / 1e6:.1f} MB)")
    print(f"AAC 128 kbps                   : {aac128:,} byte (~{aac128 / 1e6:.1f} MB, rasio ~{wav / aac128:.1f} : 1)")
    print(f"AAC  96 kbps mono              : {aac96:,} byte (~{aac96 / 1e6:.1f} MB, rasio ~{wav / aac96:.1f} : 1)")
    print(f"MP3 192 kbps                   : {mp3192:,} byte (~{mp3192 / 1e6:.1f} MB, rasio ~{wav / mp3192:.1f} : 1)")
    print()


if __name__ == "__main__":
    soal_1()
    soal_2()
    soal_3()
