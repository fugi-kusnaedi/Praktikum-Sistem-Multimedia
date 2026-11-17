"""
Praktikum Sistem Multimedia - Pertemuan 7
Langkah 1 : Membuat berkas frames.json (informasi setiap frame video).

Nama  : Fugi Kusnaedi
NIM   : 2406088
Kelas : Informatika C

Cara menjalankan (dari folder Pertemuan_7):
    python buat_frames_json.py
    python buat_frames_json.py video_lain.mp4

Keluaran:
    frames.json -> daftar frame video beserta tipe frame (I/P/B)

Catatan:
    1. Skrip memakai FFprobe bila tersedia (cara standar praktikum).
    2. Bila FFprobe tidak ada, skrip otomatis memakai FFmpeg dengan filter
       showinfo yang juga menampilkan tipe frame (type:I/P/B) dan key frame.
       FFmpeg dapat diinstal dengan `winget install Gyan.FFmpeg`.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

folder = Path(__file__).resolve().parent
file_video = folder.parent / "Pertemuan_1" / "Media_Asli" / "thanos.mp4"
file_json = folder / "frames.json"

if len(sys.argv) > 1:
    file_video = Path(sys.argv[1]).resolve()

if not file_video.exists():
    raise FileNotFoundError(f"Video tidak ditemukan: {file_video}")


def lewat_ffprobe(ffprobe, video):
    """Cara standar: ffprobe -show_frames -print_format json."""
    perintah = [
        ffprobe,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_frames",
        "-print_format", "json",
        str(video),
    ]
    proses = subprocess.run(perintah, capture_output=True, text=True, encoding="utf-8")
    if proses.returncode != 0:
        raise RuntimeError(f"FFprobe gagal:\n{proses.stderr}")
    return json.loads(proses.stdout)


def lewat_ffmpeg(ffmpeg, video):
    """Alternatif: membaca keluaran filter showinfo dari FFmpeg.

    Contoh baris keluaran:
        n:   0 pts: 0 pts_time:0 fmt:yuv420p s:640x266 i:P iskey:1 type:I ...
    """
    perintah = [
        ffmpeg, "-hide_banner", "-nostats",
        "-i", str(video),
        "-vf", "showinfo",
        "-f", "null", "-",
    ]
    proses = subprocess.run(perintah, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if proses.returncode != 0 and not proses.stderr:
        raise RuntimeError(f"FFmpeg gagal:\n{proses.stderr}")

    pola = re.compile(
        r"n:\s*(\d+)\s+pts:\s*(\S+)\s+pts_time:(\S+).*?"
        r"iskey:(\d+)\s+type:([IPB])"
    )

    frames = []
    for baris in proses.stderr.splitlines():
        cocok = pola.search(baris)
        if not cocok:
            continue
        nomor, _, pts_time, iskey, tipe = cocok.groups()
        frames.append({
            "media_type": "video",
            "key_frame": int(iskey),
            "pict_type": tipe,
            "best_effort_timestamp_time": pts_time,
            "coded_picture_number": int(nomor),
        })

    return {"frames": frames}


ffprobe = shutil.which("ffprobe")
ffmpeg = shutil.which("ffmpeg")

print("VIDEO SUMBER :", file_video)

if ffprobe:
    print("Metode       : FFprobe (-show_frames)")
    data = lewat_ffprobe(ffprobe, file_video)
elif ffmpeg:
    print("Metode       : FFmpeg (filter showinfo) - FFprobe tidak ditemukan")
    data = lewat_ffmpeg(ffmpeg, file_video)
else:
    raise RuntimeError(
        "FFprobe/FFmpeg tidak ditemukan di PATH. Instal FFmpeg lebih dahulu:\n"
        "  winget install Gyan.FFmpeg"
    )

jumlah = len(data.get("frames", []))
with open(file_json, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print(f"Berhasil menulis {jumlah} frame ke {file_json.name}")
print("Ukuran berkas :", f"{file_json.stat().st_size:,} byte")
