import subprocess 
from pathlib import Path 
 
folder = Path(".") 
 
daftar_file = [ 
    "A.wav", 
    "B.wav", 
    "C.wav", 
    "D.wav", 
    "E.wav" 
] 
 
folder_output = folder / "audio_mp3" 
folder_output.mkdir(exist_ok=True) 
 
for nama_file in daftar_file: 
    sumber = folder / nama_file 
    hasil = folder_output / f"{sumber.stem}_128k.mp3" 
 
    if not sumber.exists(): 
        print(f"File tidak ditemukan: {sumber}") 
        continue 
 
    perintah = [ 
        "ffmpeg", "-y", 
        "-i", str(sumber), 
        "-c:a", "libmp3lame", 
        "-b:a", "128k", 
        str(hasil) 
    ] 
 
    proses = subprocess.run(perintah) 
 
    if proses.returncode == 0 and hasil.exists(): 
        print(f"Berhasil: {hasil.name}") 
    else: 
        print(f"Gagal: {nama_file}")