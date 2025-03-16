import streamlit as st
import yt_dlp
import os
import shutil

# Set judul halaman
st.set_page_config(page_title="TIKTOK JOJO", page_icon="🌍")

file_path = "databasetiktok.txt"
output_path = "downloaded_videos"  # Folder penyimpanan sementara

# Buat folder jika belum ada
os.makedirs(output_path, exist_ok=True)

# Fungsi untuk membaca URL terakhir (DARI BAWAH KE ATAS)
def get_last_url():
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        if lines:
            last_line = list(reversed(lines))[0]  # Ambil baris terakhir setelah di-reverse
            return last_line.strip().split(",")[0]  # Ambil URL dari baris terakhir
    except FileNotFoundError:
        return None
    return None

# Fungsi download video
def download_tiktok_video(video_url):
    nama_vidio = video_url.replace('https://www.tiktok.com/@jojo.2801/video/','')
    """Download video dan simpan di output_path"""
    video_filename = os.path.join(output_path, "nama_vidio.mp4")  # Nama file output

    # Hapus folder video lama sebelum download baru
    if os.path.exists(output_path):
        shutil.rmtree(output_path)  # Hapus semua isi folder
    os.makedirs(output_path, exist_ok=True)  # Buat ulang folder kosong

    ydl_opts = {
        'outtmpl': video_filename,  # Simpan dengan nama tetap
        'format': 'bestvideo+bestaudio/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return video_filename
    except Exception as e:
        st.error(f"❌ Gagal download video: {e}")
        return None

# Fungsi menghapus baris terakhir dari database
def delete_last_entry():
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        if lines:
            with open(file_path, "w") as file:
                file.writelines(lines[:-1])  # Hapus baris terakhir
    except FileNotFoundError:
        pass

# Streamlit UI
st.title("📥 TikTok Video Downloader")

last_url = get_last_url()
video_filename = None

if last_url:
    st.write(f"🎥 **Video:** [Klik untuk melihat]({last_url})")

    if st.button("⬇️ Download Video"):
        video_filename = download_tiktok_video(last_url)  # Download video
        
        if video_filename:
            st.success("✅ Video berhasil di-download!")
            st.session_state['video_path'] = video_filename  # Simpan path video

# Jika ada video yang sudah di-download, tampilkan tombol download
if 'video_path' in st.session_state and os.path.exists(st.session_state['video_path']):
    with open(st.session_state['video_path'], "rb") as file:
        st.download_button(
            label="📥 Download Video",
            data=file,
            file_name="tiktok_video.mp4",
            mime="video/mp4"
        )
    
    # Hapus data terakhir setelah user download
    delete_last_entry()
