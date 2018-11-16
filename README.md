# Ijin Bot Absensi
Ijin bot telegram untuk absensi yang masih satu database dengan Face Recognition


## Installation:
    1. Install the dependencies

    2. Run VIObot.py

## Requirements:
    Python3 (3.5 ++ is recommended)

## Howto:
    `python3 VIObot.py` to run the program

    Tambahkan pada crontab -e linux untuk back up notif:
    */1 * * * * /usr/bin/python3 ~/Documents/firdauzfanani/VIO_IjinAbsensi/notif_manager.py
    */1 * * * * /usr/bin/python3 ~/Documents/firdauzfanani/VIO_IjinAbsensi/notif_karyawan.py
