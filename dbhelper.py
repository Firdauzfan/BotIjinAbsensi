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

    def get_nama_karyawan(self):
        stmt = "SELECT nama_pegawai FROM employee "
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

    def get_tele_karyawan(self,data):
        karyawan=data[1]
        stmt = "SELECT id_telegram FROM employee where nama_pegawai=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(stmt, (karyawan))
        teledapat = cursorcek.fetchone()
        getteledapat= teledapat.get('id_telegram')

        return getteledapat

    def get_data_ijin_kar(self,id_telekarya):
        ceksql= "SELECT `nama_pegawai` FROM `employee` WHERE id_telegram=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(ceksql, (id_telekarya))
        namadapat = cursorcek.fetchone()
        getnamadapat= namadapat.get('nama_pegawai')

        stmt = "SELECT nama_pegawai FROM ijin_absensi where atasan=%s AND DATE(`waktu_buat_ijin`) = DATE(CURDATE()) AND `aktif_appdpp_manager`='1'"
        cursor= self.conn.cursor()
        exc= cursor.execute(stmt, (getnamadapat))
        data= cursor.fetchall()
        return [x['nama_pegawai'] for x in data]

    def insert_data_ijin(self,data):
        id_tele=data[0]
        ijin=data[1]
        tanggal=data[2]
        manager=data[3]
        alasan_ijin=data[4]
        lampiran_tipe=data[5]
        lampiran_ijin=data[6]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        ceksql= "SELECT `nama_pegawai` FROM `employee` WHERE id_telegram=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(ceksql, (id_tele))
        namadapat = cursorcek.fetchone()
        getnamadapat= namadapat.get('nama_pegawai')

        instdata = "INSERT INTO `ijin_absensi`(`nama_pegawai`, `ijin`, `alasan_ijin`, `tanggal_ijin`, `waktu_buat_ijin`, `atasan`, `lampiran`,`tipe_lampiran`,`aktif_notif_manager`,`aktif_appdpp_manager`,`aktif_notif_karyawan`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'1','1','0')"
        cursorinst= self.conn.cursor()
        excinst= cursorinst.execute(instdata,(getnamadapat,ijin,alasan_ijin,tanggal,timestamp,manager,lampiran_ijin,lampiran_tipe))

        self.conn.commit()

        return getnamadapat

    def insert_insert_app(self,data):
        id_tele=data[0]
        nama_karyawan_ijin=data[1]
        app_dpp=data[2]
        alasan_app=data[3]

        ceksql= "SELECT `nama_pegawai` FROM `employee` WHERE id_telegram=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(ceksql, (id_tele))
        namadapat = cursorcek.fetchone()
        getnamadapat= namadapat.get('nama_pegawai')

        instdata = "UPDATE `ijin_absensi` SET `aktif_appdpp_manager`='0',`aktif_notif_karyawan`='1',`app`=%s,`app_by`=%s,`alasan_app_dpp`=%s WHERE atasan=%s AND nama_pegawai=%s AND DATE(`waktu_buat_ijin`) = DATE(CURDATE())"
        cursorinst= self.conn.cursor()
        excinst= cursorinst.execute(instdata,(app_dpp,getnamadapat,alasan_app,getnamadapat,nama_karyawan_ijin))

        self.conn.commit()

        return getnamadapat

    def check_double(self,data):
        ceksql= "SELECT `nama_pegawai` FROM `employee` WHERE id_telegram=%s"
        cursorcek= self.conn.cursor()
        cursorcek.execute(ceksql, (data))
        namadapat = cursorcek.fetchone()
        getnamadapat= namadapat.get('nama_pegawai')

        ceksqlcount= "SELECT COUNT(nama_pegawai) AS ceknama FROM `ijin_absensi` WHERE nama_pegawai=%s AND DATE(`waktu_buat_ijin`) = DATE(CURDATE())"
        cursor= self.conn.cursor()
        cursor.execute(ceksqlcount, (getnamadapat))
        checking = cursor.fetchone()

        return checking.get('ceknama')
