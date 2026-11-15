"""
Praktikum Sistem Multimedia - Pertemuan 7
Langkah 3 : Ekstraksi frame sampel dari video.

Nama  : Fugi Kusnaedi
NIM   : 2406088
Kelas : Informatika C

Cara menjalankan (dari folder Pertemuan_7):
    python ekstraksi_frame.py
    python ekstraksi_frame.py video_lain.mp4

Keluaran:
    hasil/frame_sampel/frame_<nomor>.jpg  (satu frame setiap 30 frame)

Catatan:
    Pembacaan frame dilakukan oleh video_reader.py, yang memakai OpenCV bila
    terpasang dan otomatis memakai FFmpeg bila OpenCV tidak tersedia.
"""

import sys
from pathlib import Path

from PIL import Image

from video_reader import info_video, iter_frame

folder = Path(__file__).resolve().parent
folder_sampel = folder / "hasil" / "frame_sampel"
folder_sampel.mkdir(parents=True, exist_ok=True)

file_video = folder.parent / "Pertemuan_1" / "Media_Asli" / "thanos.mp4"
if len(sys.argv) > 1:
    file_video = Path(sys.argv[1]).resolve()

if not file_video.exists():
    raise FileNotFoundError(f"Video tidak ditemukan: {file_video}")

INTERVAL = 30  # satu frame setiap 30 frame (setara 1 detik pada 30 fps)

info = info_video(file_video)
fps = info["fps"]
durasi = info["total_frame"] / fps if fps else 0

print("INFORMASI VIDEO")
print("=" * 45)
print("File        :", file_video.name)
print("Pembaca     :", info["sumber"])
print("Resolusi    :", f"{info['lebar']} x {info['tinggi']}")
print("Total frame :", info["total_frame"])
print("FPS         :", fps)
print("Durasi      :", f"{durasi:.2f} detik")
print("Interval    : setiap", INTERVAL, "frame")
print("=" * 45)

jumlah_tersimpan = 0

for nomor_frame, frame in enumerate(iter_frame(file_video, info)):
    if nomor_frame % INTERVAL != 0:
        continue

    nama_file = folder_sampel / f"frame_{nomor_frame}.jpg"
    # frame berurutan BGR -> dibalik menjadi RGB untuk disimpan oleh Pillow
    Image.fromarray(frame[:, :, ::-1]).save(nama_file, quality=90)
    print("Frame disimpan:", nama_file.name)
    jumlah_tersimpan += 1

print("=" * 45)
print("Total frame tersimpan:", jumlah_tersimpan)
print("Lokasi:", folder_sampel)
