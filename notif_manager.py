import time
import datetime
import pymysql.cursors
import time
import datetime
import os
import smtplib
import argparse
import sys
from lang_dict import *

import urllib
import telebot

TOKEN = "723437754:AAGtGSR6MUqe2mLHEYRm8MpsThaodUg7Co8"
bot = telebot.TeleBot(TOKEN)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def notif():
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         db='absensi',
                                         unix_socket="/var/run/mysqld/mysqld.sock",
                                         port=3306,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                # Create a new record
                ceksql= "SELECT COUNT(nama_pegawai) AS ceknama FROM `ijin_absensi` WHERE DATE(`waktu_buat_ijin`) = DATE(CURDATE()) AND aktif_notif_manager='1' LIMIT 1"
                cursor.execute(ceksql)
                checking = cursor.fetchone()
                print(checking.get('ceknama'))
                if checking.get('ceknama')>=1:
                    ceksql= "SELECT atasan,nama_pegawai,alasan_ijin,tanggal_ijin,ijin,tipe_lampiran,lampiran FROM `ijin_absensi` WHERE DATE(`waktu_buat_ijin`) = DATE(CURDATE()) AND aktif_notif_manager='1' LIMIT 1"
                    cursor.execute(ceksql)
                    checking = cursor.fetchone()
                    insertdata=checking.get('atasan')

                    karyawannama=checking.get('nama_pegawai')
                    alasanijin=checking.get('alasan_ijin')
                    tanggalijin=checking.get('tanggal_ijin')
                    ijinya=checking.get('ijin')
                    lampiran_tipe=checking.get('tipe_lampiran')
                    lampiran_file=checking.get('lampiran')

                    ceksqltele= "SELECT id_telegram FROM `employee` WHERE nama_pegawai=%s"
                    cursor.execute(ceksqltele, (insertdata))
                    checkingtele = cursor.fetchone()
                    idtele=checkingtele.get('id_telegram')

                    send_notif_manager(idtele,karyawannama,alasanijin,tanggalijin,ijinya,lampiran_tipe,lampiran_file)

                    sql = "UPDATE `ijin_absensi` SET `aktif_notif_manager`='0' WHERE atasan=%s AND nama_pegawai=%s AND DATE(`waktu_buat_ijin`) = DATE(CURDATE())"
                    cursor.execute(sql, (insertdata,karyawannama))
            connection.commit()
            return True

        finally:
            connection.close()

def send_notif_manager(idtele,karyawannama,alasanijin,tanggalijin,ijinya,lampiran_tipe,lampiran_file):
    if lampiran_tipe=='NULL':
        bot.send_message(chat_id=idtele, text='Karyawan dengan nama %s ingin ijin %s pada tanggal %s dengan alasan seperti berikut \n %s' %(karyawannama,ijinya,tanggalijin,alasanijin))
        bot.send_message(chat_id=idtele, text=pilih_user_konfirm[ijinya])
    elif lampiran_tipe=='Document':
        bot.send_message(chat_id=idtele, text='Karyawan dengan nama %s ingin ijin %s pada tanggal %s dengan alasan seperti berikut \n %s' %(karyawannama,ijinya,tanggalijin,alasanijin))
        bot.send_message(chat_id=idtele, text=pilih_user_konfirm[ijinya])
    elif lampiran_tipe=='Photo':
        bot.send_message(chat_id=idtele, text='Karyawan dengan nama %s ingin ijin %s pada tanggal %s dengan alasan seperti berikut \n %s' %(karyawannama,ijinya,tanggalijin,alasanijin))
        bot.send_message(chat_id=idtele, text=pilih_user_konfirm[ijinya])

notif()
