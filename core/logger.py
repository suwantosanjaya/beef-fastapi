import logging
import os
from datetime import datetime

from fastapi import Request

def get_daily_logger(name: str = "obe_logger") -> logging.Logger:
    # Folder penyimpanan log
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Format nama file log berdasarkan tanggal (YYYY-MM-DD.log)
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = os.path.join(log_dir, f"{today_str}.log")

    # Buat logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Hindari duplikasi handler jika logger sudah dibuat sebelumnya
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        formatter = logging.Formatter(
            f"%(asctime)s\t%(levelname)s\t%(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Optional: log ke console juga
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)

    return logger



def logger_request_info(request: Request = None, message: str = ""):
    logger = get_daily_logger()
    return logger.info(f"{request.method}\t{request.url}\tIP:{request.client.host}\tfrom:{request.headers.get('user-agent')}\t{message}")
