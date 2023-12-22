
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from son_uygulama import Ui_MainWindow

import sqlite3
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

baglanti = sqlite3.connect("kayit.db")
islem = baglanti.cursor()

islem.execute("""CREATE TABLE IF NOT EXISTS kayit3(
               ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               alinan_malzemenin_markasi TEXT,
               malzeme_adedi TEXT,
               malzeme_adet_fiyati TEXT,
               malzemenin_alinan_tarihi TEXT,
               malzeme_turu TEXT,
               malzemenin_ne_sekilde_depolanacagi TEXT)""")

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.lbl1.setPixmap(QtGui.QPixmap("logo.png"))


        self.listele()

        self.ekle.clicked.connect(self.ekleme)
        self.sil.clicked.connect(self.silme)

    def listele(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(("ID","alınan malzemenin markasi", "malzeme adedi", "malzeme adet fiyatı", "malzemenin alınan tarihi", "malzeme türü", "malzemenin ne şekilde depolanacağı"))

        sorgu = "SELECT * FROM kayit3"
        islem.execute(sorgu)

        for indexSatir, satirVerisi in enumerate(islem.fetchall()):
            self.table.insertRow(indexSatir)
            for indexSutun, deger in enumerate(satirVerisi):
                self.table.setItem(indexSatir, indexSutun, QTableWidgetItem(str(deger)))

    def ekleme(self):
        alinan_malzemenin_markasi = self.ln1.text()
        malzeme_adedi = self.ln2.text()
        malzeme_adet_fiyati = self.ln3.text()
        malzemenin_alinan_tarihi = self.ln4.text()
        malzemenin_ne_sekilde_depolanacagi = self.ln6.text()
        malzeme_turu = "a"


        if self.ithal.isChecked():
            malzeme_turu = 'ithal'
        elif self.radioButton_2.isChecked():
            malzeme_turu = 'yerel'

        try:
            islem.execute("INSERT INTO kayit3 (alinan_malzemenin_markasi, malzeme_adedi, malzeme_adet_fiyati, malzemenin_alinan_tarihi, malzeme_turu, malzemenin_ne_sekilde_depolanacagi) VALUES (?, ?, ?, ?, ?,?)",
              (alinan_malzemenin_markasi, malzeme_adedi, malzeme_adet_fiyati, malzemenin_alinan_tarihi, malzeme_turu, malzemenin_ne_sekilde_depolanacagi))

            baglanti.commit()
            self.statusbar.showMessage("kayit eklendi !!", 10000)
            self.listele()
        except sqlite3.Error as e:
            print("SQLite Hatası:", e)
            self.statusbar.showMessage("Kayıt eklenemedi !!", 10000)


    def guncelleme(self):
        pass



    def silme(self):
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)

        if sil_mesaj == QMessageBox.Yes:
            secilen_satir = self.table.currentRow()

            if secilen_satir >= 0:

                silinecek_kayit = self.table.item(secilen_satir, 0).text()
                sorgu = "DELETE FROM kayit3 WHERE ID= ?"

                try:
                    islem.execute(sorgu, (silinecek_kayit,))
                    baglanti.commit()
                    self.statusbar.showMessage("Kayıt silindi !!", 10000)
                    self.listele()
                except sqlite3.Error:
                    self.statusbar.showMessage("Kayıt silinemedi !!", 10000)
            else:
                self.statusbar.showMessage("Lütfen silmek istediğiniz kaydi seçin.", 10000)
        else:
            self.statusbar.showMessage("İşlem iptal edildi.", 10000)



def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

app()
baglanti.close()
