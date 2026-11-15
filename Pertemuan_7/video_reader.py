"""
Pembaca frame video untuk praktikum Pertemuan 7.

Modul ini menyediakan cara membaca frame yang sama baik OpenCV terpasang
maupun tidak:

- Jika `opencv-python` tersedia  -> memakai cv2.VideoCapture (cara modul).
- Jika tidak tersedia            -> memakai FFmpeg (rawvideo bgr24) sehingga
                                    skrip tetap dapat dijalankan.

Format frame yang dihasilkan selalu array NumPy uint8 dengan urutan kanal BGR,
sama seperti keluaran cv2.VideoCapture().read().
"""

import re
import shutil
import subprocess
from pathlib import Path

import numpy as np

try:  # OpenCV bersifat opsional
    import cv2
    ADA_OPENCV = True
except ImportError:  # pragma: no cover
    cv2 = None
    ADA_OPENCV = False


def cari_ffmpeg():
    """Mengembalikan path FFmpeg, atau None bila tidak ditemukan."""
    return shutil.which("ffmpeg")


def info_video(path):
    """Mengambil informasi dasar video: lebar, tinggi, fps, dan jumlah frame."""
    path = Path(path)

    if ADA_OPENCV:
        video = cv2.VideoCapture(str(path))
        if not video.isOpened():
            raise RuntimeError(f"Video tidak dapat dibuka: {path}")
        data = {
            "lebar": int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "tinggi": int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": float(video.get(cv2.CAP_PROP_FPS)),
            "total_frame": int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
            "sumber": "OpenCV",
        }
        video.release()
        return data

    ffmpeg = cari_ffmpeg()
    if not ffmpeg:
        raise RuntimeError(
            "OpenCV maupun FFmpeg tidak tersedia. Instal salah satu:\n"
            "  python -m pip install opencv-python\n"
            "  winget install Gyan.FFmpeg"
        )

    keluaran = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path)],
        capture_output=True, text=True, errors="replace"
    ).stderr

    durasi = 0.0
    cocok_durasi = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", keluaran)
    if cocok_durasi:
        jam, menit, detik = cocok_durasi.groups()
        durasi = int(jam) * 3600 + int(menit) * 60 + float(detik)

    cocok_stream = re.search(
        r"Video:.*?,\s*(\d{2,5})x(\d{2,5}).*?([\d.]+)\s*fps", keluaran
    )
    if not cocok_stream:
        raise RuntimeError("Informasi stream video tidak terbaca dari FFmpeg.")

    lebar, tinggi, fps = cocok_stream.groups()
    lebar, tinggi, fps = int(lebar), int(tinggi), float(fps)

    return {
        "lebar": lebar,
        "tinggi": tinggi,
        "fps": fps,
        "total_frame": int(round(durasi * fps)),
        "sumber": "FFmpeg",
    }


def iter_frame(path, info=None):
    """Menghasilkan frame video satu per satu (BGR, uint8)."""
    path = Path(path)

    if ADA_OPENCV:
        video = cv2.VideoCapture(str(path))
        if not video.isOpened():
            raise RuntimeError(f"Video tidak dapat dibuka: {path}")
        try:
            while True:
                berhasil, frame = video.read()
                if not berhasil:
                    break
                yield frame
        finally:
            video.release()
        return

    ffmpeg = cari_ffmpeg()
    if not ffmpeg:
        raise RuntimeError("OpenCV maupun FFmpeg tidak tersedia.")

    info = info or info_video(path)
    lebar, tinggi = info["lebar"], info["tinggi"]
    ukuran_frame = lebar * tinggi * 3

    proses = subprocess.Popen(
        [
            ffmpeg, "-hide_banner", "-loglevel", "error",
            "-i", str(path),
            "-f", "rawvideo", "-pix_fmt", "bgr24", "-",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    try:
        while True:
            data = proses.stdout.read(ukuran_frame)
            if len(data) < ukuran_frame:
                break
            yield np.frombuffer(data, dtype=np.uint8).reshape(tinggi, lebar, 3)
    finally:
        proses.stdout.close()
        proses.terminate()
        proses.wait(timeout=10)


def ke_grayscale(frame_bgr):
    """Konversi BGR -> grayscale (rumus luminance sama dengan cv2.COLOR_BGR2GRAY)."""
    b = frame_bgr[:, :, 0].astype(np.float32)
    g = frame_bgr[:, :, 1].astype(np.float32)
    r = frame_bgr[:, :, 2].astype(np.float32)
    return (0.114 * b + 0.587 * g + 0.299 * r).astype(np.uint8)
