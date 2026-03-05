import os
import yaml
import logging

from contextlib import contextmanager

@contextmanager
def open_file_txt(file_path, mode="a+", encoding="utf-8"):
    # Nếu file chưa tồn tại, tạo file rỗng
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Mở file (đã tồn tại hoặc vừa tạo)
    file = open(file_path, mode='a', encoding='utf-8-sig')
    try: yield file
    finally: file.close()

def open_file_yaml(file_path, mode="a+", encoding="utf-8"):
    with open(file_path, "r",encoding="utf-8-sig") as file:
        data = yaml.safe_load(file)  # Đọc xong là file sẽ tự đóng
    return data
