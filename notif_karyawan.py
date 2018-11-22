import time
import datetime
import pymysql.cursors
import time
import datetime
import os
import smtplib
import argparse
import sys

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
                ceksql= "SELECT COUNT(nama_pegawai) AS ceknama FROM `ijin_absensi` WHERE DATE(`waktu_buat_ijin`) = DATE(CURDATE()) AND aktif_notif_karyawan ='1' LIMIT 1"
                cursor.execute(ceksql)
                checking = cursor.fetchone()
                print(checking.get('ceknama'))
                if checking.get('ceknama')>=1:
                    ceksql= "SELECT atasan,nama_pegawai,alasan_app_dpp,app FROM `ijin_absensi` WHERE DATE(`waktu_buat_ijin`) = DATE(CURDATE()) AND aktif_notif_karyawan='1' LIMIT 1"
                    cursor.execute(ceksql)
                    checking = cursor.fetchone()
                    insertdata=checking.get('atasan')

                    karyawannama=checking.get('nama_pegawai')
                    alasanapp=checking.get('alasan_app_dpp')
                    appordpp=checking.get('app')

                    ceksqltele= "SELECT id_telegram FROM `employee` WHERE nama_pegawai=%s"
                    cursor.execute(ceksqltele, (karyawannama))
                    checkingtele = cursor.fetchone()
                    idtele=checkingtele.get('id_telegram')

                    send_notif_karyawan(idtele,insertdata,alasanapp,appordpp)

                    sql = "UPDATE `ijin_absensi` SET `aktif_notif_karyawan`='0' WHERE atasan=%s AND nama_pegawai=%s AND DATE(`waktu_buat_ijin`) = DATE(CURDATE())"
                    cursor.execute(sql, (insertdata,karyawannama))
            connection.commit()
            return True

        finally:
            connection.close()

def send_notif_karyawan(idtele,insertdata,alasanapp,appordpp):
    if appordpp=="APPROVE":
        appis="Menyetujui"
    elif appordpp=="DISAPPROVE":
        appis="tidak Menyetujui"

    bot.send_message(chat_id=idtele, text='Atasan anda dengan nama %s %s ijin anda dengan alasan seperti berikut \n %s' %(insertdata,appis,alasanapp))

notif()
