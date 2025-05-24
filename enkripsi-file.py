from cryptography.fernet import Fernet
import base64
import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from datetime import datetime

# Membuat folder hasil enkripsi & dekripsi jika belum ada
os.makedirs("hasil_enkripsi", exist_ok=True)
os.makedirs("hasil_dekripsi", exist_ok=True)

# Fungsi logging aktivitas ke file log_aktivitas.txt
def log_aktivitas(pesan):
    with open("log_aktivitas.txt", "a") as log:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{waktu}] {pesan}\n")

# Buat kunci manual dari teks kunci
def buat_kunci_manual(teks_kunci):
    with open("kunci_manual_text.txt", "w") as f_text:
        f_text.write(teks_kunci)

    hash_kunci = hashlib.sha256(teks_kunci.encode()).digest()
    kunci = base64.urlsafe_b64encode(hash_kunci)

    with open("kunci_manual.key", "wb") as file_kunci:
        file_kunci.write(kunci)

    log_aktivitas("Kunci manual dibuat dan disimpan")
    return kunci

# Buat kunci otomatis
def buat_kunci_otomatis():
    kunci = Fernet.generate_key()
    with open("kunci_otomatis.key", "wb") as file_kunci:
        file_kunci.write(kunci)
    log_aktivitas("Kunci otomatis dibuat dan disimpan")
    return kunci

# Membaca kunci manual
def baca_kunci_manual():
    try:
        with open("kunci_manual.key", "rb") as file_kunci:
            return file_kunci.read()
    except FileNotFoundError:
        return None

def baca_teks_kunci_manual():
    try:
        with open("kunci_manual_text.txt", "r") as f_text:
            return f_text.read()
    except FileNotFoundError:
        return None

# Membaca kunci otomatis
def baca_kunci_otomatis():
    try:
        with open("kunci_otomatis.key", "rb") as file_kunci:
            return file_kunci.read()
    except FileNotFoundError:
        return None

# Memilih kunci utama yang dipakai (manual jika ada, kalau tidak otomatis)
def baca_kunci_utama():
    kunci = baca_kunci_manual()
    return kunci if kunci else baca_kunci_otomatis()

# Fungsi enkripsi file
def enkripsi_file(nama_file):
    kunci = baca_kunci_utama()
    if not kunci:
        messagebox.showerror("Error", "Kunci belum dibuat.")
        return

    try:
        with open(nama_file, "rb") as file:
            data = file.read()

        fernet = Fernet(kunci)
        data_terenkripsi = fernet.encrypt(data)

        nama_file_output = os.path.join("hasil_enkripsi", os.path.basename(nama_file) + "_terenkripsi.dat")
        with open(nama_file_output, "wb") as file_output:
            file_output.write(data_terenkripsi)

        log_aktivitas(f"File dienkripsi: {nama_file} -> {nama_file_output}")
        messagebox.showinfo("Sukses", f"File terenkripsi:\n{nama_file_output}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal enkripsi:\n{str(e)}")

# Fungsi dekripsi file
def dekripsi_file(file_enkripsi, nama_file_output):
    kunci = baca_kunci_utama()
    if not kunci:
        messagebox.showerror("Error", "Kunci belum dibuat.")
        return

    try:
        with open(file_enkripsi, "rb") as file:
            data = file.read()

        fernet = Fernet(kunci)
        data_didekripsi = fernet.decrypt(data)

        output_path = os.path.join("hasil_dekripsi", nama_file_output)
        with open(output_path, "wb") as file_output:
            file_output.write(data_didekripsi)

        log_aktivitas(f"File didekripsi: {file_enkripsi} -> {output_path}")
        messagebox.showinfo("Sukses", f"File didekripsi:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal dekripsi:\n{str(e)}")

# GUI buat kunci manual
def buat_kunci_manual_gui():
    teks = simpledialog.askstring("Buat Kunci Manual", "Masukkan teks kunci (minimal 1 karakter):")
    if teks:
        buat_kunci_manual(teks)
        messagebox.showinfo("Sukses", "Kunci manual berhasil dibuat.")
        jendela_buat_kunci.destroy()
    else:
        messagebox.showwarning("Dibatalkan", "Pembuatan kunci dibatalkan.")

# GUI buat kunci otomatis
def buat_kunci_otomatis_gui():
    buat_kunci_otomatis()
    messagebox.showinfo("Sukses", "Kunci otomatis berhasil dibuat.")
    jendela_buat_kunci.destroy()

# GUI menu lihat kunci
def buka_menu_lihat_kunci():
    global jendela_lihat_kunci
    jendela_lihat_kunci = tk.Toplevel(root)
    jendela_lihat_kunci.title("Pilih Kunci untuk Ditampilkan")
    jendela_lihat_kunci.geometry("360x180")
    jendela_lihat_kunci.configure(bg="#2c3e50")

    label = ttk.Label(jendela_lihat_kunci, text="Pilih jenis kunci yang ingin ditampilkan:", font=("Segoe UI", 14), foreground="white", background="#2c3e50")
    label.pack(pady=15)

    btn_manual = ttk.Button(jendela_lihat_kunci, text="Lihat Kunci Manual", command=tampilkan_kunci_manual)
    btn_manual.pack(pady=10, ipadx=10, ipady=5)

    btn_otomatis = ttk.Button(jendela_lihat_kunci, text="Lihat Kunci Otomatis", command=tampilkan_kunci_otomatis)
    btn_otomatis.pack(pady=10, ipadx=10, ipady=5)

def tampilkan_kunci_manual():
    teks_asli = baca_teks_kunci_manual()
    if teks_asli:
        jendela_kunci = tk.Toplevel(root)
        jendela_kunci.title("Kunci Manual (Teks Asli)")
        jendela_kunci.geometry("520x300")

        frame = ttk.Frame(jendela_kunci, padding=15)
        frame.pack(fill="both", expand=True)

        label = ttk.Label(frame, text="Kunci Manual (Teks Asli, bisa disalin):", font=("Segoe UI", 13, "bold"))
        label.pack(pady=(0, 10))

        teks_kunci = tk.Text(frame, wrap="word", height=5, width=60, font=("Consolas", 11))
        teks_kunci.insert("1.0", teks_asli)
        teks_kunci.config(state="normal")
        teks_kunci.pack(pady=(0, 10))

        def salin_ke_clipboard():
            root.clipboard_clear()
            root.clipboard_append(teks_asli)
            messagebox.showinfo("Disalin", "Kunci telah disalin ke clipboard.")

        btn_sal = ttk.Button(frame, text="Salin ke Clipboard", command=salin_ke_clipboard)
        btn_sal.pack(side="left", padx=5)

        btn_tutup = ttk.Button(frame, text="Tutup", command=jendela_kunci.destroy)
        btn_tutup.pack(side="right", padx=5)
    else:
        messagebox.showwarning("Tidak Ada Kunci Manual", "Kunci manual belum dibuat.")
    jendela_lihat_kunci.destroy()

def tampilkan_kunci_otomatis():
    kunci = baca_kunci_otomatis()
    if kunci:
        jendela_kunci = tk.Toplevel(root)
        jendela_kunci.title("Kunci Otomatis")
        jendela_kunci.geometry("520x300")

        frame = ttk.Frame(jendela_kunci, padding=15)
        frame.pack(fill="both", expand=True)

        label = ttk.Label(frame, text="Kunci Otomatis (bisa disalin):", font=("Segoe UI", 13, "bold"))
        label.pack(pady=(0, 10))

        teks_kunci = tk.Text(frame, wrap="word", height=5, width=60, font=("Consolas", 11))
        teks_kunci.insert("1.0", kunci.decode())
        teks_kunci.config(state="normal")
        teks_kunci.pack(pady=(0, 10))

        def salin_ke_clipboard():
            root.clipboard_clear()
            root.clipboard_append(kunci.decode())
            messagebox.showinfo("Disalin", "Kunci telah disalin ke clipboard.")

        btn_sal = ttk.Button(frame, text="Salin ke Clipboard", command=salin_ke_clipboard)
        btn_sal.pack(side="left", padx=5)

        btn_tutup = ttk.Button(frame, text="Tutup", command=jendela_kunci.destroy)
        btn_tutup.pack(side="right", padx=5)
    else:
        messagebox.showwarning("Tidak Ada Kunci Otomatis", "Kunci otomatis belum dibuat.")
    jendela_lihat_kunci.destroy()

# GUI pilih file enkripsi
def pilih_file_enkripsi():
    file_path = filedialog.askopenfilename(title="Pilih file untuk dienkripsi")
    if file_path:
        enkripsi_file(file_path)

# GUI pilih file dekripsi
def pilih_file_dekripsi():
    file_path = filedialog.askopenfilename(title="Pilih file terenkripsi untuk didekripsi")
    if file_path:
        nama_output = simpledialog.askstring("Nama File Output", "Masukkan nama file hasil dekripsi (termasuk ekstensi):")
        if nama_output:
            dekripsi_file(file_path, nama_output)

# GUI menu buat kunci (diperbarui: tambah tombol Lihat Kunci)
def buka_menu_buat_kunci():
    global jendela_buat_kunci
    jendela_buat_kunci = tk.Toplevel(root)
    jendela_buat_kunci.title("Pilih Metode Buat Kunci")
    jendela_buat_kunci.geometry("360x240")
    jendela_buat_kunci.configure(bg="#34495e")

    label = ttk.Label(jendela_buat_kunci, text="Pilih metode pembuatan kunci:", font=("Segoe UI", 14), foreground="white", background="#34495e")
    label.pack(pady=15)

    btn_manual = ttk.Button(jendela_buat_kunci, text="Buat Kunci Manual", command=buat_kunci_manual_gui)
    btn_manual.pack(pady=10, ipadx=10, ipady=5)

    btn_otomatis = ttk.Button(jendela_buat_kunci, text="Buat Kunci Otomatis", command=buat_kunci_otomatis_gui)
    btn_otomatis.pack(pady=10, ipadx=10, ipady=5)

    # Tombol lihat kunci dipindahkan ke sini
    btn_lihat_kunci = ttk.Button(jendela_buat_kunci, text="Lihat Kunci", command=buka_menu_lihat_kunci)
    btn_lihat_kunci.pack(pady=10, ipadx=10, ipady=5)

# Program utama GUI
root = tk.Tk()
root.title("Program Enkripsi & Dekripsi File")
root.geometry("420x480")
root.configure(bg="#1abc9c")

# Style ttk
style = ttk.Style(root)
style.theme_use('clam')

style.configure("TButton",
                font=("Segoe UI", 12),
                padding=10)

style.configure("TLabel",
                background="#1abc9c",
                foreground="white",
                font=("Segoe UI", 16, "bold"))

# Judul
label_judul = ttk.Label(root, text="Menu Utama")
label_judul.pack(pady=(30, 20))

# Tombol menu
btn_buat_kunci = ttk.Button(root, text="Buat Kunci (Manual/Otomatis)", command=buka_menu_buat_kunci)
btn_buat_kunci.pack(fill="x", padx=40, pady=10)

# Tombol lihat kunci dihapus dari menu utama

btn_enkripsi = ttk.Button(root, text="Enkripsi File", command=pilih_file_enkripsi)
btn_enkripsi.pack(fill="x", padx=40, pady=10)

btn_dekripsi = ttk.Button(root, text="Dekripsi File", command=pilih_file_dekripsi)
btn_dekripsi.pack(fill="x", padx=40, pady=10)

btn_keluar = ttk.Button(root, text="Keluar", command=root.quit)
btn_keluar.pack(fill="x", padx=40, pady=20)

root.mainloop()
