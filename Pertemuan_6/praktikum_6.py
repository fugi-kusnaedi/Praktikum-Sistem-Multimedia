"""
Praktikum Sistem Multimedia - Pertemuan 6
Topik : Kompresi gambar (PNG / JPEG / WebP) dan evaluasi kualitas objektif
        menggunakan MSE, PSNR, dan SSIM.

Nama  : Fugi Kusnaedi
NIM   : 2406088
Kelas : Informatika C

Cara menjalankan (dari folder Pertemuan_6):
    python praktikum_6.py
    python praktikum_6.py gambar_lain.jpg

Masukan  : ../Pertemuan_5/Input.jpg  (gambar RGB)
Keluaran : hasil/  (gambar terkompresi, tabel CSV, dan grafik)

Catatan:
    MSE dan PSNR dihitung manual dengan NumPy. SSIM dihitung manual dengan
    jendela seragam 7x7 (sama seperti default scikit-image). Bila paket
    scikit-image terpasang, hasilnya sekaligus dibandingkan sebagai validasi.
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")  # grafik langsung disimpan, tidak membuka jendela
import matplotlib.pyplot as plt
from PIL import Image

try:  # opsional, hanya untuk validasi silang
    from skimage.metrics import (
        peak_signal_noise_ratio as psnr_skimage,
        structural_similarity as ssim_skimage,
    )
    ADA_SKIMAGE = True
except ImportError:
    ADA_SKIMAGE = False

# ==========================================================
# 1. PERSIAPAN FOLDER DAN GAMBAR SUMBER
# ==========================================================
folder = Path(__file__).resolve().parent
folder_hasil = folder / "hasil"
folder_hasil.mkdir(exist_ok=True)

gambar_sumber = folder.parent / "Pertemuan_5" / "Input.jpg"
if len(sys.argv) > 1:
    gambar_sumber = Path(sys.argv[1]).resolve()

if not gambar_sumber.exists():
    raise FileNotFoundError(
        f"Gambar sumber tidak ditemukan: {gambar_sumber}\n"
        "Pastikan file Pertemuan_5/Input.jpg tersedia."
    )

img = Image.open(gambar_sumber).convert("RGB")
array_asli = np.array(img)
ukuran_asli = gambar_sumber.stat().st_size

print("INFORMASI GAMBAR SUMBER")
print("=" * 50)
print("File        :", gambar_sumber.name)
print("Dimensi     :", f"{img.width} x {img.height} piksel")
print("Mode warna  :", img.mode)
print("Bentuk array:", array_asli.shape)
print("Ukuran file :", f"{ukuran_asli:,} byte")
print("Metode SSIM :", "scikit-image + manual" if ADA_SKIMAGE else "manual (NumPy)")
print("=" * 50)


# ==========================================================
# 2. KONVERSI MODEL WARNA (RGB, GRAYSCALE, HSV)
# ==========================================================
rgb = img
grayscale = img.convert("L")
hsv = img.convert("HSV")

rgb.save(folder_hasil / "gambar_rgb.png")
grayscale.save(folder_hasil / "gambar_grayscale.png")
hsv.convert("RGB").save(folder_hasil / "gambar_hsv.png")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(rgb)
axes[0].set_title("RGB")
axes[1].imshow(grayscale, cmap="gray")
axes[1].set_title("Grayscale")
axes[2].imshow(hsv.convert("RGB"))
axes[2].set_title("HSV")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
fig.savefig(folder_hasil / "perbandingan_warna.png")
plt.close(fig)

print("\nKonversi warna selesai (RGB, Grayscale, HSV).")


# ==========================================================
# 3. KOMPRESI: PNG, JPEG (10/50/90), WEBP (10/50/90)
# ==========================================================
print("\nPROSES KOMPRESI")
print("=" * 50)

file_png = folder_hasil / "gambar.png"
img.save(file_png, format="PNG", optimize=True, compress_level=9)
print(f"PNG lossless   -> {file_png.stat().st_size:,} byte")

daftar_kompresi = [(file_png, "PNG", "-", "lossless")]

for kualitas in [10, 50, 90]:
    file_jpeg = folder_hasil / f"jpeg_{kualitas}.jpeg"
    img.save(file_jpeg, format="JPEG", quality=kualitas)
    print(f"JPEG q{kualitas:<3}      -> {file_jpeg.stat().st_size:,} byte")
    daftar_kompresi.append((file_jpeg, "JPEG", str(kualitas), "lossy"))

for kualitas in [10, 50, 90]:
    file_webp = folder_hasil / f"webp_{kualitas}.webp"
    img.save(file_webp, format="WEBP", quality=kualitas)
    print(f"WebP q{kualitas:<3}      -> {file_webp.stat().st_size:,} byte")
    daftar_kompresi.append((file_webp, "WebP", str(kualitas), "lossy"))

print("=" * 50)


# ==========================================================
# 4. FUNGSI PERHITUNGAN MSE, PSNR, DAN SSIM
# ==========================================================
def hitung_mse(asli, kompresi):
    """MSE = rata-rata kuadrat selisih piksel (semua kanal)."""
    selisih = asli.astype(np.float64) - kompresi.astype(np.float64)
    return float(np.mean(selisih ** 2))


def hitung_psnr(mse, nilai_maks=255):
    """PSNR = 10 * log10(MAX^2 / MSE) dalam satuan dB."""
    if mse == 0:
        return float("inf")
    return float(10 * np.log10((nilai_maks ** 2) / mse))


def _rata_rata_jendela(data, ukuran):
    """Rata-rata tiap jendela ukuran x ukuran (hanya jendela penuh).

    Memakai integral image (cumulative sum) agar cepat tanpa SciPy.
    """
    integral = np.pad(data, ((1, 0), (1, 0)), mode="constant").cumsum(0).cumsum(1)
    tinggi, lebar = data.shape
    keluar_h = tinggi - ukuran + 1
    keluar_w = lebar - ukuran + 1

    jumlah = (
        integral[ukuran:ukuran + keluar_h, ukuran:ukuran + keluar_w]
        - integral[0:keluar_h, ukuran:ukuran + keluar_w]
        - integral[ukuran:ukuran + keluar_h, 0:keluar_w]
        + integral[0:keluar_h, 0:keluar_w]
    )
    return jumlah / (ukuran * ukuran)


def hitung_ssim_manual(asli, kompresi, ukuran_jendela=7,
                       k1=0.01, k2=0.03, nilai_maks=255):
    """SSIM manual dengan jendela seragam (default scikit-image: 7x7).

    SSIM(x, y) = ((2.mu_x.mu_y + C1)(2.sigma_xy + C2))
               / ((mu_x^2 + mu_y^2 + C1)(sigma_x^2 + sigma_y^2 + C2))
    """
    c1 = (k1 * nilai_maks) ** 2
    c2 = (k2 * nilai_maks) ** 2

    x = asli.astype(np.float64)
    y = kompresi.astype(np.float64)

    # Gambar berkanal (RGB): hitung per kanal lalu dirata-rata
    if x.ndim == 3:
        nilai = [
            hitung_ssim_manual(x[:, :, c], y[:, :, c],
                               ukuran_jendela, k1, k2, nilai_maks)
            for c in range(x.shape[2])
        ]
        return float(np.mean(nilai))

    mu_x = _rata_rata_jendela(x, ukuran_jendela)
    mu_y = _rata_rata_jendela(y, ukuran_jendela)
    mu_x2 = mu_x ** 2
    mu_y2 = mu_y ** 2
    mu_xy = mu_x * mu_y

    sigma_x2 = _rata_rata_jendela(x * x, ukuran_jendela) - mu_x2
    sigma_y2 = _rata_rata_jendela(y * y, ukuran_jendela) - mu_y2
    sigma_xy = _rata_rata_jendela(x * y, ukuran_jendela) - mu_xy

    peta_ssim = (
        (2 * mu_xy + c1) * (2 * sigma_xy + c2)
    ) / (
        (mu_x2 + mu_y2 + c1) * (sigma_x2 + sigma_y2 + c2)
    )

    return float(np.mean(peta_ssim))


def evaluasi_kompresi(file_hasil):
    """Menghitung ukuran file serta MSE, PSNR, dan SSIM hasil kompresi."""
    gambar = Image.open(file_hasil).convert("RGB")
    array = np.array(gambar)

    if array.shape != array_asli.shape:
        raise ValueError(f"Dimensi tidak sama: {file_hasil.name}")

    mse = hitung_mse(array_asli, array)
    psnr = hitung_psnr(mse)
    ssim = hitung_ssim_manual(array_asli, array)

    metrik = {
        "ukuran": file_hasil.stat().st_size,
        "mse": mse,
        "psnr": psnr,
        "ssim": ssim,
        "psnr_skimage": None,
        "ssim_skimage": None,
    }

    if ADA_SKIMAGE:
        metrik["psnr_skimage"] = float(
            psnr_skimage(array_asli, array, data_range=255)
        )
        metrik["ssim_skimage"] = float(
            ssim_skimage(array_asli, array, channel_axis=2, data_range=255)
        )

    return metrik


# ==========================================================
# 5. TABEL HASIL PERBANDINGAN
# ==========================================================
print("\nTABEL PERBANDINGAN KOMPRESI (gambar RGB)")
baris_judul = (
    f"{'Format':<8}{'Kualitas':<10}{'Ukuran (byte)':>15}"
    f"{'MSE':>12}{'PSNR (dB)':>12}{'SSIM':>10}{'Hemat (%)':>12}"
)
print("-" * len(baris_judul))
print(baris_judul)
print("-" * len(baris_judul))

data_hasil = []

for file_hasil, format_gambar, kualitas, jenis in daftar_kompresi:
    metrik = evaluasi_kompresi(file_hasil)
    hemat = (1 - metrik["ukuran"] / ukuran_asli) * 100

    data_hasil.append(
        {
            "format": format_gambar,
            "kualitas": kualitas,
            "jenis": jenis,
            "file": file_hasil.name,
            **metrik,
            "hemat": hemat,
        }
    )

    print(
        f"{format_gambar:<8}{kualitas:<10}{metrik['ukuran']:>15,}"
        f"{metrik['mse']:>12.2f}{metrik['psnr']:>12.2f}"
        f"{metrik['ssim']:>10.4f}{hemat:>12.2f}"
    )

print("-" * len(baris_judul))

# Menyimpan tabel ke CSV agar mudah disalin ke laporan
file_csv = folder_hasil / "perbandingan_kompresi.csv"
with open(file_csv, "w", encoding="utf-8") as f:
    f.write("format,kualitas,jenis,file,ukuran_byte,mse,psnr_db,ssim,hemat_persen\n")
    for d in data_hasil:
        f.write(
            f"{d['format']},{d['kualitas']},{d['jenis']},{d['file']},"
            f"{d['ukuran']},{d['mse']:.4f},{d['psnr']:.4f},"
            f"{d['ssim']:.6f},{d['hemat']:.2f}\n"
        )

print("Tabel disimpan:", file_csv.name)

if ADA_SKIMAGE:
    print("\nVALIDASI SILANG DENGAN SCIKIT-IMAGE")
    for d in data_hasil:
        print(
            f"{d['format']} q{d['kualitas']:<4} "
            f"PSNR manual {d['psnr']:7.4f} dB vs skimage {d['psnr_skimage']:7.4f} dB | "
            f"SSIM manual {d['ssim']:.6f} vs skimage {d['ssim_skimage']:.6f}"
        )


# ==========================================================
# 6. GRAFIK PSNR DAN SSIM TERHADAP UKURAN FILE (rate-distortion)
# ==========================================================
for nama_metrik, judul, satuan in [
    ("psnr", "Perbandingan PSNR terhadap Ukuran File", "PSNR (dB)"),
    ("ssim", "Perbandingan SSIM terhadap Ukuran File", "SSIM"),
]:
    fig, ax = plt.subplots(figsize=(9, 5))

    for format_gambar in ["JPEG", "WebP"]:
        data_format = [d for d in data_hasil if d["format"] == format_gambar]
        data_format.sort(key=lambda d: d["ukuran"])
        ax.plot(
            [d["ukuran"] / 1024 for d in data_format],
            [d[nama_metrik] for d in data_format],
            marker="o",
            label=format_gambar,
        )
        for d in data_format:
            ax.annotate(
                f"q{d['kualitas']}",
                (d["ukuran"] / 1024, d[nama_metrik]),
                textcoords="offset points",
                xytext=(6, 6),
                fontsize=8,
            )

    ax.set_title(judul)
    ax.set_xlabel("Ukuran File (KB)")
    ax.set_ylabel(satuan)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    fig.savefig(folder_hasil / f"grafik_{nama_metrik}.png")
    plt.close(fig)
    print(f"Grafik {nama_metrik} disimpan.")


# ==========================================================
# 7. GRAFIK UKURAN FILE PER FORMAT
# ==========================================================
fig, ax = plt.subplots(figsize=(10, 5))

label = [f"{d['format']} q{d['kualitas']}" for d in data_hasil]
nilai_kb = [d["ukuran"] / 1024 for d in data_hasil]
warna = ["gray" if d["format"] == "PNG" else
         ("tab:blue" if d["format"] == "JPEG" else "tab:orange")
         for d in data_hasil]

ax.bar(label, nilai_kb, color=warna)
ax.set_title("Ukuran File Hasil Kompresi")
ax.set_ylabel("Ukuran File (KB)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig(folder_hasil / "grafik_ukuran_file.png")
plt.close(fig)

print("Grafik ukuran file disimpan.")
print("\nSELESAI. Semua hasil ada di folder:", folder_hasil)
