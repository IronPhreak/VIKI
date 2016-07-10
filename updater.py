import os
import time
import urllib.request
import zipfile

from main import logger


def download_update(version):
    try:
        # Download Updated file
        url_prefix = "http://ironphreak.com/viki/updates/".lower()
        file_name = str(version) + ".zip"
        url = url_prefix + str(file_name)
        urllib.request.urlretrieve(url, file_name)

        # Extract Files
        logger.info("Updating to version: " + str(file_name))
        with zipfile.ZipFile(file_name, "r") as z:
            z.extractall()
        logger.info("Updating complete. Restarting VIKI")
        time.sleep(5)
        os.system("python3 /home/pi/Desktop/VIKI/main.py")
    except Exception:
        logger.error("Error: in update")
