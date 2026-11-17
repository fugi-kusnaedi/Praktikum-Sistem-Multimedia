"""
Praktikum Sistem Multimedia - Pertemuan 7
Langkah 4 : Analisis redundansi temporal dengan frame differencing.

Nama  : Fugi Kusnaedi
NIM   : 2406088
Kelas : Informatika C

Cara menjalankan (dari folder Pertemuan_7):
    python frame_differencing.py
    python frame_differencing.py video_lain.mp4

Masukan  : video (default ../Pertemuan_1/Media_Asli/thanos.mp4)
           frames.json (opsional, untuk menandai posisi I-Frame)
Keluaran : hasil/frame_differencing.png
           hasil/perbandingan_segmen.png
           hasil/frame_differencing.csv
           hasil/statistik_segmen.csv
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from video_reader import info_video, iter_frame, ke_grayscale

folder = Path(__file__).resolve().parent
folder_hasil = folder / "hasil"
folder_hasil.mkdir(exist_ok=True)

file_video = folder.parent / "Pertemuan_1" / "Media_Asli" / "thanos.mp4"
if len(sys.argv) > 1:
    file_video = Path(sys.argv[1]).resolve()

if not file_video.exists():
    raise FileNotFoundError(f"Video tidak ditemukan: {file_video}")

print("ANALISIS FRAME DIFFERENCING")
print("=" * 50)
print("Video :", file_video.name)

# ==========================================================
# 1. MENGHITUNG RATA-RATA SELISIH PIKEL ANTAR-FRAME
# ==========================================================
info = info_video(file_video)
fps = info["fps"]
total_frame = info["total_frame"]

print("Pembaca :", info["sumber"])
print(f"Frame   : {total_frame} ({info['lebar']} x {info['tinggi']}, {fps:g} fps)")

nomor_frame = []
nilai_selisih = []
frame_sebelumnya = None

for indeks, frame in enumerate(iter_frame(file_video, info)):
    gray = ke_grayscale(frame)

    if frame_sebelumnya is not None:
        selisih = np.abs(gray.astype(np.int16) - frame_sebelumnya.astype(np.int16))
        nilai_selisih.append(float(np.mean(selisih)))
        nomor_frame.append(indeks)  # nomor frame sesudahnya

    frame_sebelumnya = gray

nilai = np.array(nilai_selisih)
nomor_frame = np.array(nomor_frame)

rata_rata = float(np.mean(nilai))
median = float(np.median(nilai))
maksimum = float(np.max(nilai))
simpangan = float(np.std(nilai))
batas_lonjakan = rata_rata + 3 * simpangan
mask_lonjakan = nilai > batas_lonjakan
posisi_lonjakan = nomor_frame[mask_lonjakan]

print("\nSTATISTIK FRAME DIFFERENCING")
print("=" * 50)
print(f"Jumlah nilai selisih   : {len(nilai)}")
print(f"Rata-rata              : {rata_rata:.4f}")
print(f"Median                 : {median:.4f}")
print(f"Maksimum               : {maksimum:.4f}")
print(f"Simpangan baku         : {simpangan:.4f}")
print(f"Ambang lonjakan (x+3s) : {batas_lonjakan:.4f}")
print(f"Jumlah lonjakan        : {int(mask_lonjakan.sum())}")
print(f"Posisi lonjakan        : {posisi_lonjakan.tolist()[:25]}")
if (~mask_lonjakan).any():
    print(f"Rata-rata tanpa lonjakan: {float(np.mean(nilai[~mask_lonjakan])):.4f}")

# Menandai posisi I-Frame bila frames.json tersedia
posisi_I = []
file_json = folder / "frames.json"
if file_json.exists():
    try:
        with open(file_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except UnicodeDecodeError:
        with open(file_json, "r", encoding="utf-16") as f:
            data = json.load(f)

    tipe = [fr["pict_type"] for fr in data["frames"] if "pict_type" in fr]
    posisi_I = [i for i, t in enumerate(tipe) if t == "I"]

    if posisi_I:
        pada_I = np.isin(nomor_frame, posisi_I)
        if pada_I.any() and (~pada_I).any():
            print("\nPERBANDINGAN BERDASARKAN TIPE FRAME")
            print(f"Rata-rata selisih pada I-Frame  : {float(np.mean(nilai[pada_I])):.4f}")
            print(f"Rata-rata selisih frame lainnya : {float(np.mean(nilai[~pada_I])):.4f}")

# ==========================================================
# 2. GRAFIK FRAME DIFFERENCING
# ==========================================================
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(nomor_frame, nilai, linewidth=1, color="tab:blue", label="Rata-rata selisih")
ax.axhline(batas_lonjakan, color="red", linestyle="--", linewidth=1,
           label=f"Ambang lonjakan ({batas_lonjakan:.2f})")

if posisi_I:
    nilai_I = nilai[np.isin(nomor_frame, posisi_I)]
    ax.scatter(posisi_I[: len(nilai_I)], nilai_I, color="red", s=18,
               zorder=3, label="Posisi I-Frame")

ax.set_title("Analisis Frame Differencing")
ax.set_xlabel("Nomor Frame")
ax.set_ylabel("Rata-rata Selisih Piksel")
ax.legend()
ax.grid(True, alpha=0.4)
plt.tight_layout()
fig.savefig(folder_hasil / "frame_differencing.png")
plt.close(fig)

with open(folder_hasil / "frame_differencing.csv", "w", encoding="utf-8") as f:
    f.write("nomor_frame,rata_rata_selisih\n")
    for n, v in zip(nomor_frame, nilai):
        f.write(f"{int(n)},{v:.6f}\n")

print("\nGrafik dan CSV frame differencing disimpan.")

# ==========================================================
# 3. PERBANDINGAN SEGMEN STATIS vs DINAMIS
# ==========================================================
detik_total = total_frame / fps if fps else 0


def rentang_indeks(detik_awal, detik_akhir):
    """Mengubah rentang waktu (detik) menjadi rentang nomor frame."""
    awal = int(round(detik_awal * fps))
    akhir = int(round(min(detik_akhir, detik_total) * fps))
    return awal, akhir


SEGMEN = {
    "statis": rentang_indeks(0, 5),
    "dinamis": rentang_indeks(10, 15),
}

hasil_segmen = {}
for nama, (awal, akhir) in SEGMEN.items():
    mask = (nomor_frame >= awal) & (nomor_frame < akhir)
    nilai_segmen = nilai[mask]
    hasil_segmen[nama] = nilai_segmen

    if len(nilai_segmen):
        print(f"\nSegmen {nama} (frame {awal}-{akhir - 1}):")
        print(f"  jumlah nilai : {len(nilai_segmen)}")
        print(f"  rata-rata    : {np.mean(nilai_segmen):.4f}")
        print(f"  minimum      : {np.min(nilai_segmen):.4f}")
        print(f"  maksimum     : {np.max(nilai_segmen):.4f}")

fig, ax = plt.subplots(figsize=(11, 5))
for nama, nilai_segmen in hasil_segmen.items():
    if len(nilai_segmen):
        ax.plot(nilai_segmen, label=f"Segmen {nama.capitalize()}")
ax.set_title("Perbandingan Redundansi Temporal")
ax.set_xlabel("Urutan Frame dalam Segmen")
ax.set_ylabel("Rata-rata Selisih Piksel")
ax.legend()
ax.grid(True, alpha=0.4)
plt.tight_layout()
fig.savefig(folder_hasil / "perbandingan_segmen.png")
plt.close(fig)

with open(folder_hasil / "statistik_segmen.csv", "w", encoding="utf-8") as f:
    f.write("segmen,frame_awal,frame_akhir,jumlah_nilai,rata_rata,minimum,maksimum\n")
    for nama, nilai_segmen in hasil_segmen.items():
        awal, akhir = SEGMEN[nama]
        if len(nilai_segmen):
            f.write(f"{nama},{awal},{akhir - 1},{len(nilai_segmen)},"
                    f"{np.mean(nilai_segmen):.6f},{np.min(nilai_segmen):.6f},"
                    f"{np.max(nilai_segmen):.6f}\n")

print("\nSELESAI. Hasil disimpan di:", folder_hasil)
