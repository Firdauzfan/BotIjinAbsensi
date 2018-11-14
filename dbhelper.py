import pymysql.cursors
import time
import datetime


class DBHelper:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='absensi', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,unix_socket="/var/run/mysqld/mysqld.sock",port=3306)

    def get_nama_manager(self):
        stmt = "SELECT nama_pegawai FROM employee WHERE jabatan LIKE 'Manager%'"
        cursor= self.conn.cursor()
        exc= cursor.execute(stmt)
        data= cursor.fetchall()
        return [x['nama_pegawai'] for x in data]

    def get_tele_all(self):
        stmt = "SELECT id_telegram FROM employee"
        cursor= self.conn.cursor()
        exc= cursor.execute(stmt)
        data= cursor.fetchall()
        return [x['id_telegram'] for x in data]

    def get_tele_manager(self,data):
        manager=data[3]
        stmt = "SELECT id_telegram FROM employee where nama_pegawai=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(stmt, (manager))
        teledapat = cursorcek.fetchone()
        getteledapat= teledapat.get('id_telegram')

        return getteledapat

    def insert_data_ijin(self,data):
        id_tele=data[0]
        ijin=data[1]
        tanggal=data[2]
        manager=data[3]
        alasan_ijin=data[4]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        ceksql= "SELECT `nama_pegawai` FROM `employee` WHERE id_telegram=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(ceksql, (id_tele))
        namadapat = cursorcek.fetchone()
        getnamadapat= namadapat.get('nama_pegawai')

        instdata = "INSERT INTO `ijin_absensi`(`nama_pegawai`, `ijin`, `alasan_ijin`, `tanggal_ijin`, `waktu_buat_ijin`, `atasan`) VALUES (%s,%s,%s,%s,%s,%s)"
        cursorinst= self.conn.cursor()
        excinst= cursorinst.execute(instdata,(getnamadapat,ijin,alasan_ijin,tanggal,timestamp,manager))

        self.conn.commit()

        return getnamadapat
