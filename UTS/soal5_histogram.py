import sys
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

folder_hasil = Path("hasil")
folder_hasil.mkdir(exist_ok=True)

nama_file = sys.argv[1] if len(sys.argv) > 1 else "Input.jpg"

img = Image.open(nama_file).convert("RGB")
print("Dimensi:", img.size, "| Mode:", img.mode)

grayscale = img.convert("L")
grayscale.save(folder_hasil / "gambar_grayscale.png")

histogram_gray = grayscale.histogram()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(histogram_gray, color="gray")
ax.set_title("Histogram Grayscale Hasil Konversi")
ax.set_xlabel("Nilai Intensitas Piksel")
ax.set_ylabel("Jumlah Piksel")
plt.tight_layout()
fig.savefig(folder_hasil / "histogram_grayscale.png")
plt.show()
