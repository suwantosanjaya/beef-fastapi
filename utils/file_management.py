
import os
import uuid

from fastapi import UploadFile

def save_file(new_file: UploadFile, filename: str | None = None, upload_dir: str = "files/images") -> str:
    # Buat folder jika belum ada
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(new_file.filename)[1]
    new_filename = filename if filename else f"{uuid.uuid4().hex}{ext}"
    file_location = os.path.join(upload_dir, new_filename)
    
    # Simpan file baru
    with open(file_location, "wb") as f:
        f.write(new_file.file.read())
    return new_filename

def replace_file(new_file: UploadFile, new_filename: str | None = None, old_filename: str | None = None, upload_dir: str = "uploads/image") -> str:
    # Buat folder jika belum ada
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(new_file.filename)[1]
    new_filename = new_filename if new_filename else f"{uuid.uuid4().hex}{ext}"
    file_location = os.path.join(upload_dir, new_filename)
    
    # Simpan file baru
    with open(file_location, "wb") as f:
        f.write(new_file.file.read())
        
    # Hapus file lama jika ada
    if old_filename:
        delete_file(old_filename, upload_dir)
    return new_filename


def delete_file(filename: str, upload_dir: str):
    filepath = os.path.join(upload_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        