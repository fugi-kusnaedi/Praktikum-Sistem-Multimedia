# UTS — Praktikum Sistem Multimedia (IFRWP5149)

Kode dan bukti hasil run untuk Ujian Tengaah Semester.
**Fugi Kusnaedi — NIM 2406088 — Kelas Informatika C** — Institut Teknologi Garut, 2026.

## Daftar file

| File | Keterangan |
|---|---|
| `Input.jpg` | Gambar sumber Soal 5 (552x556 px), disalin dari `Pertemuan_5/Input.jpg` |
| `verifikasi_uts.py` | Perhitungan Soal 1 (PCM), Soal 2 (ringkas), estimasi Soal 3 |
| `soal2_rle_huffman.py` | Soal 2 lengkap: adaptasi `Pertemuan_3/rle.py` + `Pertemuan_3/hufman.py` (tie-breaker `itertools.count()` pada heap) |
| `soal5_histogram.py` | Soal 5: buka RGB -> grayscale -> histogram (Pillow + Matplotlib) |
| `hasil/output_soal1.txt` | Output asli `verifikasi_uts.py` |
| `hasil/output_soal2.txt` | Output asli `soal2_rle_huffman.py` |
| `hasil/output_soal5.txt` | Output asli `soal5_histogram.py Input.jpg` |
| `hasil/gambar_grayscale.png` | Hasil konversi grayscale (oleh `soal5_histogram.py`) |
| `hasil/histogram_grayscale.png` | Gambar 1 laporan — dirender `soal5_histogram.py` |
| `hasil/bukti/` | Salinan bukti dari Pertemuan_4/5/6/7 (tidak diubah) — lihat `hasil/bukti/SUMBER.md` |

## Cara menjalankan

```bash
cd UTS
python3 verifikasi_uts.py                      | tee hasil/output_soal1.txt
python3 soal2_rle_huffman.py                   | tee hasil/output_soal2.txt
MPLBACKEND=Agg python3 soal5_histogram.py Input.jpg | tee hasil/output_soal5.txt
```

Dependensi: Python 3, Pillow, NumPy, Matplotlib (di Termux: `pkg install python-numpy matplotlib python-pillow`).

## Pemetaan Soal -> file

| Soal | Isi | File/hasil |
|---|---|---|
| 1 (10 poin) | ASCII vs UTF-8; ukuran PCM mono 5 s, 44.100 Hz, 16-bit | `verifikasi_uts.py` -> `output_soal1.txt` (220.500 sampel; 3.528.000 bit; **441.000 byte = 430,7 KiB**) |
| 2 (15 poin) | RLE, kode Huffman, rata-rata panjang kode, rasio | `soal2_rle_huffman.py` -> `output_soal2.txt` (RLE `4A3B2C1D` 64 bit; Huffman 19 bit; A=0, B=10, C=111, D=110; rata-rata 1,90; entropi 1,8464; efisiensi 97,2%) |
| 3 (15 poin) | Konversi podcast WAV -> AAC | **Dilewati**: `podcast.wav` tidak ada di repo. Estimasi ukuran ada di `output_soal1.txt` (bagian SOAL 3) |
| 4 (15 poin) | Trade-off JPEG vs WebP (PSNR/SSIM) | Bukti: `hasil/bukti/soal4_*` (dari `Pertemuan_6`, angka COCOK target) |
| 5 (10 poin) | Pillow: RGB, grayscale, histogram | `soal5_histogram.py` -> `output_soal5.txt` + `hasil/histogram_grayscale.png` |
| 6 (10 poin) | Frame I/P/B, GOP, redundansi temporal | Bukti: `hasil/bukti/soal6_*` (data lama `Pertemuan_7`) + **re-run ASLI dari `thanos.mp4` di `soal6/`** (skrip P7 disalin, 539 frame, output di `soal6/hasil/` & `hasil/output_soal6_*.txt`). Angka laporan final (760 frame) berasal dari `ZekGanteng.mp4` yang tidak tersedia — detail `hasil/bukti/SUMBER.md` |
| 7 (25 poin) | DCT, energy compaction, kaitan JPEG | Konseptual (Bagian B); didukung pembahasan Soal 4 |

## Catatan integritas data

- Semua angka berasal dari run asli atau data repo; tidak ada yang dibulatkan/disesuaikan.
- Soal 6: video `ZekGanteng.mp4` tidak tersimpan di repo, sehingga verifikasi ulang
  760 frame tidak dapat dilakukan dari sumber; selisih data dilaporkan terbuka
  di `hasil/bukti/SUMBER.md`.
