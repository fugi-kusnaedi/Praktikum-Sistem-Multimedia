"""
Praktikum Sistem Multimedia - Pertemuan 7
Langkah 2 : Analisis struktur GOP dan distribusi frame I/P/B.

Nama  : Fugi Kusnaedi
NIM   : 2406088
Kelas : Informatika C

Cara menjalankan (dari folder Pertemuan_7):
    python pertemuan7.py

Masukan  : frames.json (dibuat oleh buat_frames_json.py)
Keluaran : hasil/distribusi_frame.png
           hasil/struktur_gop.png
           hasil/distribusi_frame.csv
           hasil/struktur_gop.csv
"""

import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent
folder_hasil = folder / "hasil"
folder_hasil.mkdir(exist_ok=True)
file_json = folder / "frames.json"


def baca_frames_json(path):
    """Membaca frames.json dengan deteksi encoding.

    FFprobe yang dijalankan lewat redirect PowerShell dapat menghasilkan
    berkas UTF-16, sehingga perlu fallback ke UTF-16.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except UnicodeDecodeError:
        with open(path, "r", encoding="utf-16") as file:
            return json.load(file)


if not file_json.exists():
    raise FileNotFoundError(
        "frames.json tidak ditemukan. Jalankan dulu: python buat_frames_json.py"
    )

data = baca_frames_json(file_json)
frames = data["frames"]

# Hanya frame video yang memiliki atribut pict_type (frame audio tidak punya)
tipe_frame = [frame["pict_type"] for frame in frames if "pict_type" in frame]

jumlah = Counter(tipe_frame)
jumlah_I = jumlah.get("I", 0)
jumlah_P = jumlah.get("P", 0)
jumlah_B = jumlah.get("B", 0)
total = len(tipe_frame)

# ==========================================================
# 1. DISTRIBUSI FRAME I/P/B
# ==========================================================
print("DISTRIBUSI FRAME VIDEO")
print("=" * 45)
print(f"{'Tipe Frame':<12}{'Jumlah':>10}{'Persentase':>15}")
print("-" * 45)
for nama, nilai in [("I-Frame", jumlah_I), ("P-Frame", jumlah_P), ("B-Frame", jumlah_B)]:
    persen = (nilai / total * 100) if total else 0
    print(f"{nama:<12}{nilai:>10}{persen:>14.2f}%")
print("-" * 45)
print(f"{'Total':<12}{total:>10}{100:>14.2f}%")
print("=" * 45)

fig, ax = plt.subplots(figsize=(8, 5))
label = ["I-Frame", "P-Frame", "B-Frame"]
nilai = [jumlah_I, jumlah_P, jumlah_B]
batang = ax.bar(label, nilai, color=["tab:red", "tab:blue", "tab:green"])
for b, v in zip(batang, nilai):
    ax.text(
        b.get_x() + b.get_width() / 2, v, f"{v}\n({v / total * 100:.1f}%)",
        ha="center", va="bottom", fontsize=9
    )
ax.set_title("Distribusi Frame I/P/B")
ax.set_xlabel("Tipe Frame")
ax.set_ylabel("Jumlah Frame")
ax.set_ylim(0, max(nilai) * 1.2)
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig(folder_hasil / "distribusi_frame.png")
plt.close(fig)

with open(folder_hasil / "distribusi_frame.csv", "w", encoding="utf-8") as f:
    f.write("tipe_frame,jumlah,persentase\n")
    for nama, v in [("I", jumlah_I), ("P", jumlah_P), ("B", jumlah_B)]:
        f.write(f"{nama},{v},{v / total * 100:.2f}\n")
    f.write(f"TOTAL,{total},100.00\n")

# ==========================================================
# 2. STRUKTUR GOP
# ==========================================================
# Satu GOP dimulai oleh I-Frame dan berakhir tepat sebelum I-Frame berikutnya.
posisi_I = [i for i, t in enumerate(tipe_frame) if t == "I"]
panjang_gop = []
for urut, awal in enumerate(posisi_I):
    akhir = posisi_I[urut + 1] if urut + 1 < len(posisi_I) else total
    panjang_gop.append(akhir - awal)

print("\nSTRUKTUR GOP")
print("=" * 55)
print(f"Jumlah GOP        : {len(posisi_I)}")
print(f"Posisi I-Frame    : {posisi_I}")
print(f"Panjang GOP (min) : {min(panjang_gop)}")
print(f"Panjang GOP (max) : {max(panjang_gop)}")
print(f"Panjang GOP (rata): {sum(panjang_gop) / len(panjang_gop):.2f}")
print("=" * 55)

# 20 frame pertama beserta tipenya
print("\nTIPE 20 FRAME PERTAMA")
for i in range(min(20, total)):
    print(f"Frame ke-{i:<4} : {tipe_frame[i]}-Frame")

# Tabel GOP (maksimal 30 GOP pertama agar ringkas)
print("\nTABEL GOP (30 GOP pertama)")
print(f"{'GOP ke-':<10}{'Frame awal':>12}{'Frame akhir':>13}{'Panjang':>10}")
print("-" * 45)
for urut, (awal, panjang) in enumerate(zip(posisi_I, panjang_gop), start=1):
    if urut > 30:
        print("...")
        break
    print(f"{urut:<10}{awal:>12}{awal + panjang - 1:>13}{panjang:>10}")

with open(folder_hasil / "struktur_gop.csv", "w", encoding="utf-8") as f:
    f.write("gop_ke,frame_awal,frame_akhir,panjang_gop\n")
    for urut, (awal, panjang) in enumerate(zip(posisi_I, panjang_gop), start=1):
        f.write(f"{urut},{awal},{awal + panjang - 1},{panjang}\n")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(range(1, len(panjang_gop) + 1), panjang_gop, color="tab:purple")
ax.set_title("Panjang Setiap GOP")
ax.set_xlabel("GOP ke-")
ax.set_ylabel("Jumlah Frame")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig(folder_hasil / "struktur_gop.png")
plt.close(fig)

# ==========================================================
# 3. POLA URUTAN FRAME PADA GOP PERTAMA
# ==========================================================
pola = "".join(tipe_frame[: min(panjang_gop[0], 30)])
print("\nPOLA GOP PERTAMA (maks. 30 frame):", pola)

print("\nSELESAI. Grafik dan tabel tersimpan di:", folder_hasil)
