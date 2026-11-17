# SUMBER.md — Asal-usul file bukti di folder ini

Semua file di folder `bukti/` adalah **salinan mentah (tidak diubah)** dari hasil
praktikum sebelumnya. Tidak ada angka yang diedit atau "disesuaikan".

## Soal 4 — JPEG vs WebP (disalin dari Pertemuan_6)

| File di folder ini | Salinan dari | Keterangan |
|---|---|---|
| `soal4_grafik_ukuran_file.png` | `Pertemuan_6/hasil/grafik_ukuran_file.png` | Grafik ukuran file vs kualitas |
| `soal4_grafik_psnr.png` | `Pertemuan_6/hasil/grafik_psnr.png` | Grafik PSNR vs kualitas |
| `soal4_grafik_ssim.png` | `Pertemuan_6/hasil/grafik_ssim.png` | Grafik SSIM vs kualitas |
| `soal4_perbandingan_kompresi.csv` | `Pertemuan_6/hasil/perbandingan_kompresi.csv` | Data mentah pengukuran |

Dibuat oleh `praktikum_6.py` pada sumber PNG `gambar.png` (295.440 byte).
**Cek terhadap target laporan: COCOK.**

- PNG sumber = 295.440 B (OK)
- JPEG 90 = 45.139 B, PSNR 50,4003 dB, SSIM 0,997119 (OK)
- WebP 90 = 37.880 B, PSNR 42,7886 dB, SSIM 0,983777 (OK, 16,1% lebih kecil dari JPEG)
- WebP 10: hemat 71,66%, SSIM 0,867610 (laporan menulis ~0,868) (OK)
- JPEG 10: PSNR 29,5400 dB (OK)

## Soal 5 — Histogram (Gambar 1 utama BUKAN dari sini)

- Gambar utama Soal 5 (`UTS/hasil/histogram_grayscale.png` dan `gambar_grayscale.png`)
  **dirender oleh `UTS/soal5_histogram.py` sendiri** (matplotlib, MPLBACKEND=Agg),
  bukan salinan dari Pertemuan_5.
- `soal5_histogram_pertemuan5_pembanding.png` = salinan
  `Pertemuan_5/hasil/histogram_grayscale.png` (dibuat `praktikum_5.py`),
  hanya sebagai **pembanding**.

## Soal 6 — GOP / frame differencing (disalin dari Pertemuan_7)

| File di folder ini | Salinan dari | Dibuat oleh |
|---|---|---|
| `soal6_frame_diff.png` | `Pertemuan_7/hasil/frame_differencing.png` | `frame_differencing.py` |
| `soal6_struktur_gop.png` | `Pertemuan_7/hasil/struktur_gop.png` | `pertemuan7.py` |
| `soal6_distribusi_frame.png` | `Pertemuan_7/hasil/distribusi_frame.png` | `pertemuan7.py` |
| `soal6_perbandingan_segmen.png` | `Pertemuan_7/hasil/perbandingan_segmen.png` | `frame_differencing.py` |
| `soal6_frame_differencing.csv` | `Pertemuan_7/hasil/frame_differencing.csv` | `frame_differencing.py` |
| `soal6_distribusi_frame.csv` | `Pertemuan_7/hasil/distribusi_frame.csv` | `pertemuan7.py` |
| `soal6_struktur_gop.csv` | `Pertemuan_7/hasil/struktur_gop.csv` | `pertemuan7.py` |
| `soal6_statistik_segmen.csv` | `Pertemuan_7/hasil/statistik_segmen.csv` | `frame_differencing.py` |

**Cek terhadap target laporan final: TIDAK COCOK.** Data Pertemuan_7 yang tersimpan
di repo adalah **versi lama** (dari video 539 frame), sedangkan laporan final menulis
hasil analisis video 760 frame:

| Item | Target laporan final | Data repo (apa adanya) |
|---|---|---|
| Total frame | 760 | 539 |
| I / P / B | 26 / 202 / 532 | 37 / 137 / 365 |
| Jumlah GOP | 26 | 37 |
| Rata-rata selisih piksel | 2,65 | 2,13 |
| Lonjakan ekstrem | 106-108 di frame 203-204 dan 383-384 | 15-35 di frame 273-280 |
| Segmen statis 0-5 s | 2,11 | 2,309 (frame 0-149) |
| Segmen dinamis 10-15 s | 3,49 (2,07 tanpa lonjakan) | 2,019 (frame 300-449) |

Video sumber (`ZekGanteng.mp4`) **tidak tersimpan di repo** (hanya CSV/PNG/JSON hasil
analisisnya), sehingga analisis tidak dapat diulang untuk memverifikasi angka 760
frame dari sumber aslinya. Sesuai aturan: **angka tidak diubah, tidak dibuat grafik
simulasi**; salinan grafik versi lama dipertahankan sebagai bukti, dan selisihnya
dilaporkan terbuka seperti di atas.

## Soal 3 — Audio/FFmpeg: DILEWATI

`podcast.wav` **tidak ada di repo** (folder Pertemuan_4 hanya berisi A.wav-E.wav
untuk latihan batch encoding). Sesuai aturan, konversi tidak dibuat dan tidak ada
file simulasi. Perhitungan estimasi ukuran (tanpa file) tetap tersedia di
`hasil/output_soal1.txt` (bagian SOAL 3 pada `verifikasi_uts.py`).

---

# PEMBARUAN: Re-run analisis Soal 6 (2026-11-17)

Karena video sumber laporan final (`ZekGanteng.mp4`, 760 frame) **tidak tersimpan
di repo maupun device**, analisis Soal 6 diulang dari nol menggunakan video yang
memang menjadi sumber data repo, yaitu **`Pertemuan_1/Media_Asli/thanos.mp4`**
(539 frame, 640x266, 30 fps — diverifikasi `ffprobe -count_frames`).

## Skrip & hasil re-run: `UTS/soal6/`

| File | Keterangan |
|---|---|
| `buat_frames_json.py`, `pertemuan7.py`, `frame_differencing.py`, `video_reader.py` | Salinan skrip Pertemuan_7 (tidak diubah isinya), dijalankan di folder ini |
| `frames.json` | HASIL RUN BARU: 539 frame via `ffprobe -show_frames` (470.491 byte) |
| `hasil/distribusi_frame.csv/.png` | HASIL RUN BARU: I=37, P=137, B=365, total 539 |
| `hasil/struktur_gop.csv/.png` | HASIL RUN BARU: 37 GOP, rata-rata panjang 14,57 |
| `hasil/frame_differencing.csv/.png` | HASIL RUN BARU: 538 nilai selisih |
| `hasil/statistik_segmen.csv`, `perbandingan_segmen.png` | HASIL RUN BARU |
| `../hasil/output_soal6_frames.txt` | Output asli `buat_frames_json.py` (tee) |
| `../hasil/output_soal6_gop.txt` | Output asli `pertemuan7.py` (tee) |
| `../hasil/output_soal6_diff.txt` | Output asli `frame_differencing.py` (tee) |

**Angka re-run (apa adanya, dari `output_soal6_diff.txt`):**

| Item | Nilai re-run (thanos.mp4) |
|---|---|
| Total frame | 539 |
| I / P / B | 37 / 137 / 365 (6,86% / 25,42% / 67,72%) |
| Jumlah GOP | 37 (rata-rata panjang 14,57) |
| Rata-rata selisih piksel | 2,1358 (median 1,7508; maksimum 34,756) |
| Lonjakan (ambang x+3s = 11,85) | 9 buah, posisi frame 272-280 |
| Rata-rata tanpa lonjakan | 1,7944 |
| Selisih pada I-Frame vs lainnya | 5,5256 vs 1,8927 |
| Segmen statis (frame 0-149) | 2,3124 |
| Segmen dinamis (frame 300-449) | 2,0278 |

Catatan: angka re-run konsisten dengan CSV lama Pertemuan_7 (selisih kecil, mis.
2,1358 vs 2,13) karena pembaca frame berbeda (FFmpeg pipe vs OpenCV).

**Kesimpulan integritas:** angka 760 frame, lonjakan 106-108 pada frame 203-204
dan 383-384, serta nilai 2,65 / 6,66 / 1,95 / 2,11 / 3,49 di laporan final hanya
dapat dihasilkan dari `ZekGanteng.mp4`, yang tidak tersedia. Jika video tersebut
disediakan, pipeline di `UTS/soal6/` tinggal dijalankan ulang dengan argumen
video tersebut (`python3 buat_frames_json.py <video>`, dst.) untuk memverifikasinya.
