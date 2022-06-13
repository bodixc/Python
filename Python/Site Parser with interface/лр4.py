import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from pathlib import Path
import time
import urllib

class Parser(QObject):
    change = pyqtSignal()
    BO_count = 0
    isRun = True
    def Parser(self):
        self.connect = sqlite3.Connection("лр4.db")
        abbr = ["вул.","ал.","пров.","вулиця","просп.","Вул."]
        self.BO_number = 0
        self.School_number = 0
        cursor = self.connect.cursor()
        cursor.execute(f'SELECT "Кількість опрацьованих ВО" FROM "Регіони України" WHERE "Назва регіону" = "{region}"')
        v = cursor.fetchone()
        self.BO_number = int(v[0])
        cursor.close()       
        cursor = self.connect.cursor()
        cursor.execute(f'SELECT "Кількість опрацьованих шкіл" FROM "Регіони України" WHERE "Назва регіону" = "{region}"')
        s = cursor.fetchone()
        self.School_number = int(s[0])
        cursor.close()       
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')
        div = soup.select_one('#admin-struct').select_one('ul').select_one('li').select_one('li').select_one('ul')
        ul = div.find_all('a')
        self.BO_count = len(ul)
        if self.BO_number != 0:
            del ul[:self.BO_number-1]
        for li in ul:
            if self.isRun == True:
                self.BO = li.text
                href = li.get('href')
                url_BO = url + href
                req = requests.get(url_BO)
                soup_BO = BeautifulSoup(req.text, features='html.parser')
                try:
                    ul_BO = soup_BO.select_one('#main-content').find_all('li')
                except:
                    continue
                try:
                    a = ul_BO[1].select_one('a')
                except:
                    continue
                try:
                    text = a.text
                except:
                    continue
                if 'ЗЗСО ' in text:
                    href_BO = a.get('href').strip()
                    url_33CO = url + href_BO
                    reque = requests.get(url_33CO)
                    soup_schools = BeautifulSoup(reque.text, features='html.parser')
                    try:
                        schools_tr = soup_schools.select_one('table', class_ = 'zebra-stripe list').find_all('tr')
                
                    except:
                        continue
                    del schools_tr[0]
                    if self.School_number != 0:
                        del schools_tr[:self.School_number]
                    for tr in schools_tr:
                        if self.isRun == True:
                            td = tr.find_all('td')
                            try:
                                a_school = td[1].select_one('a')
                            except:
                                continue
                            self.School = a_school.text.strip()
                            href_school = a_school.get('href')
                            url_school = url + href_school
                            request = requests.get(url_school)
                            soup_info = BeautifulSoup(request.text, features='html.parser')
                            try:
                                info_tr = soup_info.select_one('table', class_ = 'zebra-stripe').find_all('tr')
                            except:
                                continue
                            system_number = ""
                            full_name = ""
                            short_name = ""
                            address = ""
                            code_koatyy = ""
                            telephone = ""
                            email = ""
                            site = ""
                            director  = ""
                            students = ""
                            id_region = ""
                            katott = ""
                            address = ""
                            for info in info_tr:
                                info_th = info.select_one('th')
                                info_td = info.select_one('td')
                                try:
                                    text = info_th.text
                                except:
                                    continue
                                value = info_td.text
                                if '№ у системі:' in text:
                                    system_number = value
                                    system_number = system_number.strip()
                                elif 'Повна назва:' in text:
                                    full_name = value
                                    full_name = full_name.strip()
                                    full_name = full_name.replace("\""," ")
                                elif 'Скорочена:' in text:
                                    short_name = value
                                    short_name = short_name.strip()
                                    short_name = short_name.replace("\""," ")
                                elif 'Поштова адреса:' in text:
                                    post_address = value
                                    post_address = post_address.strip()
                                elif 'Код КОАТУУ:' in text:
                                    code_koatyy = value
                                    code_koatyy = code_koatyy.strip()
                                elif 'Телефони:' in text:
                                    telephone = value
                                    telephone = telephone.strip()
                                elif 'E-mail:' in text:
                                    try:
                                        a = info.select_one('td').select_one('a')
                                        a = str(a)
                                        a = a[61:-45]
                                        href = urllib.parse.unquote(a)
                                        soup_2 = BeautifulSoup(href,features = 'html.parser')
                                        email = soup_2.select_one('a').text
                                    except:
                                        continue
                                elif 'Сайт(и):' in text:
                                    site = value
                                    site = site.strip()
                                elif 'Директор:' in text:
                                    director = value
                                    director = director.strip()
                                elif 'Кількість учнів:' in text:
                                    students = value
                                    students = students.strip()
                            cursor = self.connect.cursor()
                            cursor.execute(f'SELECT "ID регіону" FROM "Регіони України" WHERE "Назва регіону" = "{region}"')
                            d = cursor.fetchone()
                            id_region = d[0]
                            cursor.close()       
                            cursor = self.connect.cursor()
                            cursor.execute(f'SELECT "КАТОТТГ" FROM "Перехідна таблиця з КОАТУУ на КАТОТТГ" WHERE "КОАТУУ" = "{code_koatyy}"')
                            c = cursor.fetchone()
                            cursor.close()
                            try:
                                katott = c[0]
                            except:
                                pass
                            for i in abbr:
                                if i in post_address:
                                    address = post_address[post_address.index(i):]
                            cursor = self.connect.cursor()
                            query = f'''INSERT INTO "Школи" ("№ у системі", "Повна назва", "Скорочена", "Поштова адреса", "Код КОАТУУ", 
                            "Телефони", "E-mail", "Сайт(и)", "Директор", "Кількість учнів", "Регіон", "Код КАТОТТГ","Адреса") 
                            values ("{system_number}","{full_name}","{short_name}","{post_address}","{code_koatyy}",
                                    "{telephone}","{email}","{site}","{director}","{students}","{id_region}","{katott}","{address}")'''
                            cursor.execute(query)
                            cursor.close()
                            self.connect.commit()
                            self.School_number += 1
                            self.change.emit()
                            cursor = self.connect.cursor()
                            cursor.execute(f'update "Регіони України" set "Кількість опрацьованих шкіл" = {self.School_number} where "Назва регіону" like \'{region}\' ')
                            cursor.close()
                            self.connect.commit()
                            time.sleep(2
                                       )
                self.School_number = 0
                self.BO_number += 1
                cursor = self.connect.cursor()
                cursor.execute(f'update "Регіони України" set "Кількість опрацьованих ВО" = {self.BO_number} where "Назва регіону" like \'{region}\' ')
                cursor.close()
                self.connect.commit()
        self.connect.close()
        
    def stop(self):
        self.isRun = False
        
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        self.move(400, 320)
    
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Left panel
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        central_layout.addWidget(self.left_widget)

        # Right panel
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        central_layout.addWidget(right_widget)
        self.connect = sqlite3.Connection("лр4.db")
        cursor = self.connect.cursor()
        sql = 'SELECT "Назва регіону" FROM "Регіони України"'
        cursor.execute(sql)
        a = cursor.fetchall()
        cursor.close()
        self.regions = list()
        for i in a:
            self.regions.append(i[0])
        cursor = self.connect.cursor()
        sql3 = 'SELECT "ID регіону" FROM "Регіони України"'
        cursor.execute(sql3)
        c = cursor.fetchall()
        cursor.close()
        self.id_regions = list()
        for i in c:
            self.id_regions.append(i[0])
        cursor = self.connect.cursor()  
        sql2 = 'SELECT "Вебадреса сторінки регіону на сайті isuo.org" FROM "Регіони України"'
        cursor.execute(sql2)
        b = cursor.fetchall()
        cursor.close()
        self.urls = list()
        for i in b:
            self.urls.append(i[0])
        self.combo = QComboBox()
        self.combo.addItems(self.regions)
        right_layout.addWidget(self.combo)

        btn_start = QPushButton()
        btn_start.setText('Start')
        self.do_stop = False
        btn_start.clicked.connect(self.start)
        right_layout.addWidget(btn_start)

        btn_stop = QPushButton()
        btn_stop.setText('Stop')
        btn_stop.clicked.connect(self.stop)
        right_layout.addWidget(btn_stop)

        self.label = QLabel(self)
        self.label.setText("")
        right_layout.addWidget(self.label)
        self.progress = QProgressBar()
        right_layout.addWidget(self.progress)

        right_layout.addStretch()

        menu_file = self.menuBar().addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        # exit_action.triggered.connect(app.quit)
        # exit_action.setDisabled(True)
        menu_file.addAction(exit_action)

        self.show()
        self.activateWindow()
        
        self.label1 = QLabel(self)
        self.label1.setText("КАТОТТГ")
        self.left_layout.addWidget(self.label1)
        self.edit_KATOTT = QLineEdit()
        self.left_layout.addWidget(self.edit_KATOTT)
        
        btn_import1 = QPushButton()
        btn_import1.setText('Import')
        btn_import1.clicked.connect(self.import_1)
        self.left_layout.addWidget(btn_import1)
        
        self.label2 = QLabel(self)
        self.label2.setText("Перехідна таблиця з КОАТУУ на КАТОТТГ")
        self.left_layout.addWidget(self.label2)
        self.edit_table_KOAT_KATOTT = QLineEdit()
        self.left_layout.addWidget(self.edit_table_KOAT_KATOTT)
        
        btn_import2 = QPushButton()
        btn_import2.setText('Import')
        btn_import2.clicked.connect(self.import_2)
        self.left_layout.addWidget(btn_import2)
        
        self.label3 = QLabel(self)
        self.label3.setText("Поле пошуку")
        self.left_layout.addWidget(self.label3)
        self.edit_search = QLineEdit()
        self.left_layout.addWidget(self.edit_search)
        
        btn_search = QPushButton()
        btn_search.setText('Пошук')
        btn_search.clicked.connect(self.search)
        self.left_layout.addWidget(btn_search)
        self.table = QTableWidget(self)
        self.table.setHorizontalHeaderLabels(["№", "Школа", "Адреса"])
        self.table.setColumnCount(3)
        self.left_layout.addWidget(self.table)
        self.left_layout.addStretch()
                
        self.TH = QThread()
            
    def start(self):
        global url,region
        url = self.urls[self.combo.currentIndex()]
        region = self.regions[self.combo.currentIndex()]
        id_region = self.id_regions[self.combo.currentIndex()]
        self.parser = Parser()
        self.parser.moveToThread(self.TH)
        self.TH.started.connect(self.parser.Parser)
        self.parser.change.connect(self.set_progress)
        self.TH.start()
    def set_progress(self):
        self.progress.setRange(1, self.parser.BO_count)
        self.progress.setValue(self.parser.BO_number + 1)
        self.label.setText(self.parser.BO + ": " + self.parser.School)
    
    def stop(self):
        self.TH.quit()
        self.parser.stop()
        
    def import_1(self):
        df = pd.read_excel(self.edit_KATOTT.text())
        df_region = df[df[df.columns[5]] == 'O']
        df_region = df_region.reset_index(drop=True)
        count_row = df_region.shape[0]
        connect = sqlite3.Connection("лр4.db")
        cursor = connect.cursor()
        try:
            cursor.execute('CREATE TABLE "КАТОТТГ - Регіони" ("Код І рівня" TEXT,"Регіон" TEXT)')
        except:
            cursor.execute('DROP TABLE "КАТОТТГ - Регіони"')
            cursor.execute('CREATE TABLE "КАТОТТГ - Регіони" ("Код І рівня" TEXT,"Регіон" TEXT)')
        for i in range(count_row):
            query = f'insert into "КАТОТТГ - Регіони" ("Код І рівня","Регіон") values ("{df_region.loc[i][0]}","{df_region.loc[i][6]}")'
            cursor.execute(query)
        connect.commit()

        df_raion = df[df[df.columns[5]] == 'P']
        df_raion = df_raion.reset_index(drop=True)
        count_row = df_raion.shape[0]
        connect = sqlite3.Connection("лр4.db")
        cursor = connect.cursor()
        try:
            cursor.execute('CREATE TABLE "КАТОТТГ - Райони" ("Код І рівня" TEXT,"Код ІІ рівня" TEXT,"Район" TEXT)')
        except:
            cursor.execute('DROP TABLE "КАТОТТГ - Райони"')
            cursor.execute('CREATE TABLE "КАТОТТГ - Райони" ("Код І рівня" TEXT,"Код ІІ рівня" TEXT,"Район" TEXT)')
        for i in range(count_row):
            query = f'insert into "КАТОТТГ - Райони" ("Код І рівня","Код ІІ рівня","Район") values ("{df_raion.loc[i][0]}","{df_raion.loc[i][1]}","{df_raion.loc[i][6]}")'
            cursor.execute(query)
        connect.commit()

        df_nas = df[df[df.columns[5]] != 'P']
        df_nas = df_nas[df_nas[df_nas.columns[5]] != 'O']
        df_nas = df_nas.reset_index(drop=True)
        count_row = df_nas.shape[0]
        connect = sqlite3.Connection("лр4.db")
        cursor = connect.cursor()
        try:
            cursor.execute('CREATE TABLE "КАТОТТГ - Населені пункти" ("Код І рівня" TEXT, "Код ІІ рівня" TEXT, "Код ІІІ рівня" TEXT, "Код ІV рівня" TEXT, "Код населеного пункту" TEXT, "Населений пункт" TEXT, "Адреса" TEXT)')
        except:
            cursor.execute('DROP TABLE "КАТОТТГ - Населені пункти"')
            cursor.execute('CREATE TABLE "КАТОТТГ - Населені пункти" ("Код І рівня" TEXT, "Код ІІ рівня" TEXT, "Код ІІІ рівня" TEXT, "Код ІV рівня" TEXT, "Код населеного пункту" TEXT, "Населений пункт" TEXT, "Адреса" TEXT)')
        for i in range(2,count_row-3):
            query = f'insert into "КАТОТТГ - Населені пункти" ("Код І рівня", "Код ІІ рівня", "Код ІІІ рівня", "Код ІV рівня", "Код населеного пункту", "Населений пункт", "Адреса") values ("{df_nas.loc[i][0]}","{df_nas.loc[i][1]}","{df_nas.loc[i][2]}","{df_nas.loc[i][3]}","{df_nas.loc[i][5]}","{df_nas.loc[i][6]}","")'
            cursor.execute(query)
        connect.commit()

        cursor = connect.cursor()
        query = '''
        SELECT NAS."Код ІV рівня", "Регіон"||' область, '||"Район"||' район, '||"Скорочення"||' '||"Населений пункт" as "Адреса" from "КАТОТТГ - Населені пункти" as NAS 
        INNER JOIN "КАТОТТГ - Райони" as RAY on RAY."Код ІІ рівня" = NAS."Код ІІ рівня"
        INNER JOIN "КАТОТТГ - Регіони" as REG on REG."Код І рівня" = RAY."Код І рівня"
        INNER JOIN "Розшифровка коду населеного пункту" as ROZ on NAS."Код населеного пункту" = ROZ."Код населеного пункту"
        WHERE NAS."Код населеного пункту" != 'H'
        '''
        cursor.execute(query)
        table = cursor.fetchall()
        for i in range(len(table)):
             cursor = connect.cursor()
             query = f'UPDATE "КАТОТТГ - Населені пункти" SET "Адреса" = \'{table[i][1]}\' where "Код ІV рівня" = \'{table[i][0]}\' '
             cursor.execute(query)
             cursor.close()
        connect.commit()

        cursor = connect.cursor()
        query = '''
        SELECT NAS."Код ІІІ рівня", NAS."Код ІV рівня", "Регіон"||' область, '||"Район"||' район, '||"Скорочення"||' '||"Населений пункт" as "Адреса" from "КАТОТТГ - Населені пункти" as NAS 
        INNER JOIN "КАТОТТГ - Райони" as RAY on RAY."Код ІІ рівня" = NAS."Код ІІ рівня"
        INNER JOIN "КАТОТТГ - Регіони" as REG on REG."Код І рівня" = RAY."Код І рівня"
        INNER JOIN "Розшифровка коду населеного пункту" as ROZ on NAS."Код населеного пункту" = ROZ."Код населеного пункту"
        WHERE NAS."Код населеного пункту" = 'H'
        '''
        cursor.execute(query)
        table = cursor.fetchall()
        cursor.close()
        for i in range(len(table)):
             cursor = connect.cursor()
             query = f'UPDATE "КАТОТТГ - Населені пункти" SET "Адреса" = \'{table[i][2]}\' where "Код ІV рівня" = \'nan\' and "Код ІІІ рівня" = \'{table[i][0]}\' '
             cursor.execute(query)
             cursor.close()
        connect.commit()
        connect.close()
        
    def import_2(self):
        df = pd.read_excel(self.edit_table_KOAT_KATOTT.text())
        count_row = df.shape[0]
        connect = sqlite3.Connection("лр4.db")
        cursor = connect.cursor()
        try:
            cursor.execute('CREATE TABLE "Перехідна таблиця з КОАТУУ на КАТОТТГ" ("КОАТУУ" TEXT,"КАТОТТГ" TEXT)')
        except:
            cursor.execute('DROP TABLE "Перехідна таблиця з КОАТУУ на КАТОТТГ"')
            cursor.execute('CREATE TABLE "Перехідна таблиця з КОАТУУ на КАТОТТГ" ("КОАТУУ" TEXT,"КАТОТТГ" TEXT)')
        for i in range(count_row-1):
            query = f'insert into "Перехідна таблиця з КОАТУУ на КАТОТТГ" ("КОАТУУ","КАТОТТГ") values ("{df.loc[i][0]}","{df.loc[i][3]}")'
            cursor.execute(query)
        connect.commit()
        connect.close()
        
    def search(self):
        connect = sqlite3.Connection("лр4.db")
        cursor = connect.cursor()
        cursor.execute(f'SELECT "Код ІV рівня","Адреса" FROM "КАТОТТГ - Населені пункти" where "Населений пункт" like "%{self.edit_search.text()}%"')
        nas = cursor.fetchall()
        cursor.close()
        school_list = list()
        cursor = connect.cursor()
        for i in range(len(nas)):
            cursor.execute(f'SELECT "№ у системі","Скорочена" FROM "Школи" where "Код КАТОТТГ" = "{nas[i][0]}"')
            school = cursor.fetchall()
            for i in range(len(school)):
                school_list.append([school[i][0],school[i][1],nas[i][1]])
        connect.close()
        self.table.setRowCount(len(school_list))
        for i in range(len(school_list)):
            self.table.setItem(i, 0, QTableWidgetItem(school_list[i][0]))
            self.table.setItem(i, 1, QTableWidgetItem(school_list[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(school_list[i][2]))
        self.table.resizeColumnsToContents()

        
app = QApplication(sys.argv)
win = MainWindow()
app.exec()