import sys, dbhandler, os, json, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QDialog, QTableWidgetItem, QVBoxLayout, QPushButton, QLabel, QTextBrowser, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QColor, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('src/ui/mainwindow.ui', self)
        self.dbname = 'info.db'
        dbhandler.create_database(self.dbname)
        dbhandler.evalDb(self.dbname)

        self.readyTable()
        self.circmanbtn.clicked.connect(self.goManCirc)
        self.mancircbackbtn.clicked.connect(self.setHome)
        self.addncbtn.clicked.connect(self.addNewCircular)
        self.modcircbtn.clicked.connect(self.modCircular)
        self.fullcirc.itemDoubleClicked.connect(self.modCircular)
        self.fullapp.itemDoubleClicked.connect(self.modNewApp)
        self.fullex.itemDoubleClicked.connect(self.modExam)
        self.modexbtn.clicked.connect(self.modExam)
        self.minicirc.itemDoubleClicked.connect(self.goManCirc)
        self.miniapp.itemDoubleClicked.connect(self.goManApp)
        self.miniexam.itemDoubleClicked.connect(self.goManEx)
        self.manappbackbtn.clicked.connect(self.setHome)
        self.appmanbtn.clicked.connect(self.goManApp)
        self.modappbtn.clicked.connect(self.modNewApp)
        self.exmanbtn.clicked.connect(self.goManEx)
        self.manexbackbtn.clicked.connect(self.setHome)
        self.congbackbtn.clicked.connect(self.setHome)
        self.delbtn3.clicked.connect(self.deleteExam)
        self.delbtn2.clicked.connect(self.deleteApp)
        self.actionArchive.triggered.connect(self.goArc)
        self.actionAbout.triggered.connect(self.goAbout)
        self.actionHelp.triggered.connect(self.goHelp)
        self.arcbackbtn.clicked.connect(self.setHome)
        self.delbtn.clicked.connect(self.delCirc)
        self.addnebtn.clicked.connect(self.addNewExam)
        self.nobtn.clicked.connect(self.addNewExam)
        self.yesbtn.clicked.connect(self.send2arc)



        self.setHome()

    def send2arc(self):
        dbhandler.move2arc(self.dbname, self.exampassid)
        self.goArc()


    def setHome(self):
        dbhandler.evalDb(self.dbname)
        self.popMinicirc()
        self.popMiniapp()
        self.popMiniex()

        self.stack.setCurrentWidget(self.homepage)


    def popMiniex(self):
        self.miniexam.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Exams')

        for row_data in data:
            name, extype, date, venue, result = row_data[2], row_data[5], row_data[6], row_data[7], row_data[-1]

            row_position = self.miniexam.rowCount()
            self.miniexam.insertRow(row_position)

            exdate = QDate.fromString(date, Qt.ISODate)
            today = QDate.currentDate()
            dayleft = today.daysTo(exdate)

            item1 = QTableWidgetItem(name)
            item2 = QTableWidgetItem(extype)
            item3 = QTableWidgetItem(exdate.toString('dd/MM/yyyy'))
            item4 = QTableWidgetItem(venue)

            if dayleft > 5:
                item5 = QTableWidgetItem(f'{dayleft} days')
            elif 0 < dayleft <= 5:
                item5 = QTableWidgetItem(f'{dayleft} days')
                item5.setBackground(QColor(Qt.yellow))
            elif dayleft == 0:
                item5 = QTableWidgetItem(f'Exam Day')
                item5.setBackground(QColor('#ffcc80'))
            elif dayleft < 0 and result == 'Pending':
                item5 = QTableWidgetItem('Pending')
                item5.setBackground(QColor("#ff8566"))
            elif dayleft < 0 and result == 'Passed':
                item5 = QTableWidgetItem('Passed')
                item5.setBackground(QColor('#8cff66'))
            else:
                item5 = QTableWidgetItem('Failed')
                item5.setBackground(QColor(Qt.red))

            items = [item1, item2, item3, item4, item5]

            i = 0
            for item in items:
                item.setTextAlignment(Qt.AlignCenter)
                self.miniexam.setItem(row_position, i, item)
                i += 1


    def popMiniapp(self):
        self.miniapp.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Applications')

        for row_data in data:
            name, designation, category, schedule = row_data[2], row_data[4], row_data[3], row_data[-1]

            row_position = self.miniapp.rowCount()
            self.miniapp.insertRow(row_position)
            item1 = QTableWidgetItem(name)
            item2 = QTableWidgetItem(designation)
            item3 = QTableWidgetItem(category)
            item4 = QTableWidgetItem(schedule)
            
            if schedule == 'Yes':
                item4.setBackground(QColor(Qt.yellow))
            items = [item1, item2, item3, item4]
            
            i=0
            for item in items:
                item.setTextAlignment(Qt.AlignCenter)
                self.miniapp.setItem(row_position, i, item)
                i += 1


    def popMinicirc(self):
        self.minicirc.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Circulars')
        today = QDate.currentDate()

        for row_data in data:
            short_name, designation, last_date, status = row_data[2], row_data[3], row_data[-2], row_data[-1]
            last_date = QDate.fromString(last_date, Qt.ISODate)
            days_difference = today.daysTo(last_date)

            # Calculate availability based on days difference
            if today == last_date:
                availability = 'Last Day'
                item3 = QTableWidgetItem(availability)
                item3.setBackground(QColor(Qt.yellow))
            elif today > last_date:
                availability = 'Expired'
                item3 = QTableWidgetItem(availability)
                item3.setBackground(QColor(Qt.red))
            else:
                availability = f'{days_difference} Days'
                item3 = QTableWidgetItem(availability)
                item3.setBackground(QColor(Qt.green))

            # Insert data into table
            row_position = self.minicirc.rowCount()
            self.minicirc.insertRow(row_position)
            item1 = QTableWidgetItem(short_name)
            item2 = QTableWidgetItem(designation)
            item4 = QTableWidgetItem(status)

            if status == 'Pending':
                item4.setBackground(QColor(Qt.yellow))
            else:
                item4.setBackground(QColor(Qt.green))

            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            item3.setTextAlignment(Qt.AlignCenter)
            item4.setTextAlignment(Qt.AlignCenter)

            self.minicirc.setItem(row_position, 0, item1)
            self.minicirc.setItem(row_position, 1, item2)
            self.minicirc.setItem(row_position, 2, item3)
            self.minicirc.setItem(row_position, 3, item4)     


    def goManEx(self):
        dbhandler.evalDb(self.dbname)
        self.fullex.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Exams')
        pendingexam = 0
        pendingresult = 0
        self.examids = []

        for row_num, row_data in enumerate(data):
            self.fullex.insertRow(row_num)
            examid, appid, *row_data = row_data
            self.examids.append(examid)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))

                if col_num == 4:
                    date = QDate.fromString(str(col_data), Qt.ISODate)
                    formatted_date = date.toString('dd/MM/yyyy')
                    item = QTableWidgetItem(formatted_date)
                
                item.setTextAlignment(Qt.AlignCenter)
                self.fullex.setItem(row_num, col_num, item)

            result = row_data[-1]
            today = QDate.currentDate()

            dayleft = today.daysTo(date)

            if dayleft > 5:
                pendingexam += 1
                item = QTableWidgetItem(f'{dayleft} days')
            elif 0 < dayleft <= 5:

                pendingexam += 1
                item = QTableWidgetItem(f'{dayleft} days')
                item.setBackground(QColor(Qt.yellow))
            elif dayleft == 0:
                pendingresult += 1
                item = QTableWidgetItem(f'Exam Day')
                item.setBackground(QColor('#ffcc80'))
            elif dayleft < 0 and result == 'Pending':
                pendingresult += 1
                item = QTableWidgetItem('Pending Result')
                item.setBackground(QColor("#ff8566"))
            elif dayleft < 0 and result == 'Passed':
                item = QTableWidgetItem('Passed')
                item.setBackground(QColor('#8cff66'))
            else:
                item = QTableWidgetItem('Failed')
                item.setBackground(QColor(Qt.red))

            item.setTextAlignment(Qt.AlignCenter)
            self.fullex.setItem(row_num, 6, item)

        self.pendinglabel3.setText(f'Pending Exam: {pendingexam} \t Pending Result: {pendingresult}')
        self.stack.setCurrentWidget(self.manexpage)


    def goManApp(self):
        dbhandler.evalDb(self.dbname)
        self.fullapp.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Applications')
        pendingexam = 0
        self.appids = []
        for row_num, row_data in enumerate(data):
            self.fullapp.insertRow(row_num)
            appid, _, *row_data = row_data
            self.appids.append(appid)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))

                if col_num == 3:
                    date = QDate.fromString(str(col_data), Qt.ISODate)
                    formatted_date = date.toString('dd/MM/yyyy')
                    item = QTableWidgetItem(formatted_date)

                item.setTextAlignment(Qt.AlignCenter)
                self.fullapp.setItem(row_num, col_num, item)

            
            schedule = row_data[-1]
            item = QTableWidgetItem(schedule)
            if schedule == 'Yes':
                item.setBackground(QColor(Qt.yellow))
                item.setTextAlignment(Qt.AlignCenter)
                self.fullapp.setItem(row_num, 6, item)
            else:
                pendingexam += 1

        self.pendinglabel2.setText(f'Pending Exams Announcement: {pendingexam}')
        self.stack.setCurrentWidget(self.manapppage)
                

    def goManCirc(self):
        dbhandler.evalDb(self.dbname)
        self.fullcirc.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Circulars')
        today = QDate.currentDate()
        pendingfee = 0
        paidfee = 0
        self.circids = []
        for row_num, row_data in enumerate(data):
            self.fullcirc.insertRow(row_num)
            circid, *row_data = row_data
            self.circids.append(circid) 
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))


                # Formatting date columns ('Published', 'Start Date', 'Last Date')
                if col_num in [ 4, 5]:  # Assuming columns 3, 4, 5 correspond to dates
                    date = QDate.fromString(str(col_data), Qt.ISODate)
                    formatted_date = date.toString('dd/MM/yyyy')
                    item = QTableWidgetItem(formatted_date)
                
                item.setTextAlignment(Qt.AlignCenter)
                self.fullcirc.setItem(row_num, col_num, item)

            # Calculate Availability based on current date and Last Date
            last_date = QDate.fromString(row_data[5], Qt.ISODate)  # Assuming 'Last Date' is at index 5
            days_difference = today.daysTo(last_date)

            if today == last_date:
                availability = 'Last Day'
                item = QTableWidgetItem(availability)
                item.setBackground(QColor(Qt.yellow))
            elif today > last_date:
                availability = 'Expired'
                item = QTableWidgetItem(availability)
                item.setBackground(QColor(Qt.red))
            else:
                availability = f'{days_difference} Days'
                item = QTableWidgetItem(availability)
                item.setBackground(QColor(Qt.green))

            # Set calculated Availability in the 'Availability' column (index 6)
            item.setTextAlignment(Qt.AlignCenter)
            self.fullcirc.setItem(row_num, 6, item)

            # Set Status column (assuming 'Status' is the last column)
            status = row_data[-1]  # Assuming 'Status' is the last item in the fetched data
            item = QTableWidgetItem(status)
            if status == "Pending":
                pendingfee += int(row_data[3])
                item.setBackground(QColor(Qt.yellow))

            else:
                paidfee += int(row_data[3])
                item.setBackground(QColor(Qt.green))
            item.setTextAlignment(Qt.AlignCenter)
            self.fullcirc.setItem(row_num, 7, item)

        self.pendinglabel.setText(f'Pending Fee: {pendingfee} Taka \t Paid Fee: {paidfee} Taka')

        self.stack.setCurrentWidget(self.mancircpage)


    def modCircular(self):
        try:
            rowNumber = self.fullcirc.currentRow()
            circid = self.circids[rowNumber]
            row_data = dbhandler.getDataRow(self.dbname, 'Circulars', 'CircularID', circid)
            circularid, *data_values = row_data

            # Column names (assuming the order matches the JSON format)
            column_names = ['fullname', 'shortname', 'designation', 'appfee', 'startdate', 'lastdate', 'status']

            # Create a dictionary using column names and row data
            data = dict(zip(column_names, data_values))

            # Save data to JSON file
            with open('clip.bin', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            
            status1 = data['status']

            dialog = NewCircDialog(self)
            dialog.exec_()

            if os.path.exists('clip.bin'):            
                with open('clip.bin', 'r') as file:
                    data = json.load(file)
                

                if data['status'] == 'Applied' and status1 != 'Applied':
                    dialog = NewAppDiag(self)
                    dialog.exec_()

                    if os.path.exists('clip.bin'):
                        with open('clip.bin', 'r') as file:
                            data1 = json.load(file)

                        if data1['schedule'] == 'Yes':
                            dialog = NewExDiag(self)
                            dialog.exec_()
                            if os.path.exists('clip.bin'):
                                with open('clip.bin', 'r') as file:
                                    data2 = json.load(file)
                            dbhandler.modCircular(self.dbname, circularid, data)
                            appid=dbhandler.newApplication(self.dbname, circularid, data1)
                            _=dbhandler.newExam(self.dbname, appid, data2)
                            os.remove('clip.bin') 

                        else:
                            dbhandler.modCircular(self.dbname, circularid, data)
                            _=dbhandler.newApplication(self.dbname, circularid, data1)                        
                            os.remove('clip.bin')
                            
                else:
                    os.remove('clip.bin')
                    dbhandler.modCircular(self.dbname,circularid,data)
                self.goManCirc()
        except:
            pass
        

    def addNewCircular(self):
        dialog = NewCircDialog(self)
        dialog.exec_()

        if os.path.exists('clip.bin'):          
            with open('clip.bin', 'r') as file:
                data = json.load(file)
            

            if data['status'] == 'Applied':
                dialog = NewAppDiag(self)
                dialog.exec_()
                if os.path.exists('clip.bin'):
                    with open('clip.bin', 'r') as file:
                        data1 = json.load(file)

                    if data1['schedule'] == 'Yes':
                        dialog = NewExDiag(self)
                        dialog.exec_()
                        if os.path.exists('clip.bin'):
                            with open('clip.bin', 'r') as file:
                                data2 = json.load(file)
                            circularid = dbhandler.newCircular(self.dbname, data)
                            appid=dbhandler.newApplication(self.dbname, circularid, data1)
                            _=dbhandler.newExam(self.dbname, appid, data2)
                            os.remove('clip.bin')


                    else:    
                        circularid = dbhandler.newCircular(self.dbname, data)
                        _=dbhandler.newApplication(self.dbname, circularid, data1)
                        os.remove('clip.bin')                        
                        
            else:
                os.remove('clip.bin')
                _ = dbhandler.newCircular(self.dbname,data)
            self.goManCirc()

    def modExam(self):
        try:
            rowNumber = self.fullex.currentRow()
            examid = self.examids[rowNumber]

            row_data = dbhandler.getDataRow(self.dbname, 'Exams', 'ExamID', examid)

            _,_, *data_values = row_data

            col_names = ['shortname', 'category', 'rollno', 'extype', 'exdate', 'venue', 'result']

            # Create a dictionary using column names and row data
            data = dict(zip(col_names, data_values))

            result = data['result']

            # Save data to JSON file
            with open('clip.bin', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            dialog = NewExDiag()
            dialog.exec_()

            if os.path.exists('clip.bin'):
                with open('clip.bin', 'r') as json_file:
                    data = json.load(json_file)
                
                if data['result'] == 'Passed' and result != 'Passed':
                    os.remove('clip.bin')
                    dbhandler.modExam(self.dbname, examid, data)
                    self.exampassid = examid
                    self.stack.setCurrentWidget(self.congrats)
                        
                else:
                    dbhandler.modExam(self.dbname, examid, data)
                    os.remove('clip.bin')
                    self.goManEx()
            else:
                self.goManEx()
            
        except:
            pass

    def addNewExam(self):
        try:
            try:
                rowNumber = self.fullex.currentRow()
                examid = self.examids[rowNumber]

                row_data = dbhandler.getDataRow(self.dbname, 'Exams', 'ExamID', examid)

                _,appid, *data_values = row_data

                col_names = ['shortname', 'category', 'rollno']

                dtv = [data_values[0], data_values[1], data_values[2]]

                # Create a dictionary using column names and row data
                data = dict(zip(col_names, dtv))

                # Save data to JSON file
                with open('clip.bin', 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                dialog = NewExDiag()
                dialog.exec_()

                if os.path.exists('clip.bin'):
                    with open('clip.bin', 'r') as json_file:
                        data = json.load(json_file)
                    if data['result'] == 'Passed':
                        self.exampassid=dbhandler.newExam(self.dbname, appid, data)
                        os.remove('clip.bin')
                        self.stack.setCurrentWidget(self.congrats)
                    else:                
                        _=dbhandler.newExam(self.dbname, appid, data)
                        os.remove('clip.bin')
                        self.setHome()
            except:
                rowNumber = self.fullapp.currentRow()
                appid = self.appids[rowNumber]
                row_data = dbhandler.getDataRow(self.dbname, 'Applications', 'ApplicationID', appid)
                appid, circularid, *data_values = row_data

                column_names = ['shortname', 'category', 'designation', 'appdate', 'regno', 'note', 'schedule']

                # Create a dictionary using column names and row data
                data = dict(zip(column_names, data_values))

                # Save data to JSON file
                with open('clip.bin', 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                dialog = NewExDiag()
                dialog.exec_()

                if os.path.exists('clip.bin'):
                    with open('clip.bin', 'r') as json_file:
                        data = json.load(json_file)
                    if data['result'] == 'Passed':
                        self.exampassid=dbhandler.newExam(self.dbname, appid, data)
                        os.remove('clip.bin')
                        self.stack.setCurrentWidget(self.congrats)
                    else:                
                        _=dbhandler.newExam(self.dbname, appid, data)
                        os.remove('clip.bin')
                        self.setHome()


        except:
            pass


    def modNewApp(self):
        try:
            rowNumber = self.fullapp.currentRow()
            appid = self.appids[rowNumber]
            row_data = dbhandler.getDataRow(self.dbname, 'Applications', 'ApplicationID', appid)
            appid, circularid, *data_values = row_data


            column_names = ['shortname', 'category', 'designation', 'appdate', 'regno', 'note', 'schedule']

            # Create a dictionary using column names and row data
            data = dict(zip(column_names, data_values))

            # Save data to JSON file
            with open('clip.bin', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            schedule = data['schedule']

            dialog = NewAppDiag(self)
            dialog.exec_()

            if os.path.exists('clip.bin'):
                with open('clip.bin', 'r') as file:
                    data = json.load(file)

                dbhandler.modApplication(self.dbname, appid, data)
                os.remove('clip.bin')
                if data['schedule'] == 'Yes' and schedule != 'Yes':                   
                    self.addNewExam()
                else:
                    self.goManApp()                       

            else:        
                self.goManApp()
        except:
            pass

    def delCirc(self):
        try:
            rowNumber = self.fullcirc.currentRow()
            circid = self.circids[rowNumber]
            dbhandler.delCircular(self.dbname, circid)
            self.goManCirc()

        except:
            pass

        
    def deleteExam(self):
        try:
            rowNumber = self.fullex.currentRow()
            examid = self.examids[rowNumber]
            dbhandler.delExam(self.dbname, examid)
            self.goManEx()

        except:
            pass

    
    def deleteApp(self):
        try:
            rowNumber = self.fullapp.currentRow()
            appid = self.appids[rowNumber]
            dbhandler.delApp(self.dbname, appid)
            self.goManApp()

        except:
            pass

    def readyTable(self):
        self.minicirc.setColumnCount(4)
        self.minicirc.setHorizontalHeaderLabels(["Organisation","Post","Availability","Status"])
        self.minicirc.horizontalHeader().setStyleSheet("::section { background-color: #b3ecff; }")
        for i in range(self.minicirc.columnCount()):
            self.minicirc.horizontalHeader().setSectionResizeMode(i,QHeaderView.Stretch)


        self.fullcirc.setColumnCount(8)
        self.fullcirc.setHorizontalHeaderLabels(['Full Name','Short Name', 'Post', 'Application Fee', 'Start Date', 'Last Date', 'Availability', 'Status'])
        self.fullcirc.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.fullcirc.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.fullcirc.horizontalHeader().resizeSection(1,150)
        self.fullcirc.horizontalHeader().resizeSection(3,150)
        self.fullcirc.horizontalHeader().resizeSection(4,150)
        self.fullcirc.horizontalHeader().resizeSection(5,150)
        self.fullcirc.horizontalHeader().resizeSection(6,150)
        self.fullcirc.horizontalHeader().resizeSection(7,150)
        self.fullcirc.horizontalHeader().setStyleSheet("::section { background-color: cyan; }")
        


        self.miniapp.setColumnCount(4)
        self.miniapp.setHorizontalHeaderLabels(["Organisation","Post","Category","Schedule"])
        self.miniapp.horizontalHeader().setStyleSheet("::section { background-color: #ccffcc; }")
        for i in range(self.miniapp.columnCount()):
            self.miniapp.horizontalHeader().setSectionResizeMode(i,QHeaderView.Stretch)      


        self.fullapp.setColumnCount(7)
        self.fullapp.setHorizontalHeaderLabels(['Organisation', 'Category', 'Post', 'Application Date', 'Registration No', 'Note', 'Schedule'])
        # Set all columns to stretch to fill the available space
        for i in range(7):
            self.fullapp.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        # Set background color for header sections
        self.fullapp.horizontalHeader().setStyleSheet("::section { background-color: cyan; }")


        self.miniexam.setColumnCount(5)
        self.miniexam.setHorizontalHeaderLabels(["Organisation","Type","Date","Venue", "Remarks"])
        self.miniexam.horizontalHeader().setStyleSheet("::section { background-color: #ffb3b3; }")
        for i in range(self.miniexam.columnCount()):
            self.miniexam.horizontalHeader().setSectionResizeMode(i,QHeaderView.Stretch)

        self.fullex.setColumnCount(7)
        self.fullex.setHorizontalHeaderLabels(['Organisation', 'Category', 'Roll', 'Type', 'Date', 'Venue', 'Result'])
        # Set all columns to stretch to fill the available space
        for i in range(7):
            self.fullex.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        # Set background color for header sections
        self.fullex.horizontalHeader().setStyleSheet("::section { background-color: cyan; }")

        self.arctable.setColumnCount(10)
        self.arctable.setHorizontalHeaderLabels(['Full Name', 'Short Name', 'Post', 'Applied On', 'Fee', 'ExamType', 'Venue', 'Result', 'Outcome', 'Note'])
        # Set all columns to stretch to fill the available space
        # for i in range(10):
        #     self.arctable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.arctable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.arctable.horizontalHeader().resizeSection(2,200)
        # Set background color for header sections
        self.arctable.horizontalHeader().setStyleSheet("::section { background-color: cyan; }")

    def goArc(self):

        dbhandler.evalDb(self.dbname)
        self.arctable.setRowCount(0)
        data = dbhandler.getData(self.dbname, 'Archive')
        today = QDate.currentDate()

        # pendingfee = 0
        paidfee = 0
        self.circids = []
        scslist = []
        for row_num, row_data in enumerate(data):
            self.arctable.insertRow(row_num)
            circid,_, *row_data = row_data
            # self.circids.append(circid) 
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))


                # Formatting date columns ('Published', 'Start Date', 'Last Date')
                if col_num == 3:  # Assuming columns 3, 4, 5 correspond to dates
                    date = QDate.fromString(str(col_data), Qt.ISODate)
                    formatted_date = date.toString('dd/MM/yyyy')
                    item = QTableWidgetItem(formatted_date)

                if col_num == 7:
                    if col_data == 'Failed':
                        item.setBackground(QColor('#ff9999'))
                    elif col_data == 'Passed':
                        item.setBackground(QColor('#4dff4d'))

                if col_num == 8:
                    if col_data == 'Expired':
                        item.setBackground(QColor('#ff9999'))
                    elif col_data == 'Success!':
                        item.setBackground(QColor('#4dff4d'))
                        scslist.append(row_num)



                if col_num == 4:
                    if circid not in self.circids and row_data[-2] != 'Expired':
                        self.circids.append(circid)
                        try:
                            paidfee += int(col_data)
                        except:
                            pass

                
                item.setTextAlignment(Qt.AlignCenter)
                self.arctable.setItem(row_num, col_num, item)
        
        for row in scslist:
            for col in range(10):
                item = self.arctable.item(row,col)
                item.setBackground(QColor('#66ff66'))

        self.arcpend.setText(f'Total money spent: {paidfee} Taka')

        self.stack.setCurrentWidget(self.arcPage)


    def goAbout(self):
        dialog = AboutDialog()
        dialog.exec_()

    def goHelp(self):
        dialog = HelpDialog()
        dialog.exec_()

    def resizeEvent(self, event):
        current_size = self.size()
        width=current_size.width()
        height=current_size.height()
        self.stack.setGeometry(0,0,width,height-50)
        super().resizeEvent(event)


class NewExDiag(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loadUi('src/ui/nedialog.ui',self)
        try:
            with open('clip.bin', 'r') as file:
                data = json.load(file)
            os.remove('clip.bin')
            self.company.setText(data['shortname'])
            self.catbox.setText(data['category'])
            if 'rollno' in data:
                self.roll.setText(data['rollno'])

            # Check if 'regno' key exists in data before accessing it
            if 'extype' in data and data['extype']:
                self.exambox.setCurrentText(data['extype'])

            if 'exdate' in data:
                self.exdate.setDate(QDate.fromString(data['exdate'], Qt.ISODate))
            else:
                self.exdate.setDate(QDate.currentDate())
            
            # Check if 'note' key exists in data before accessing it
            if 'venue' in data and data['venue']:
                self.venue.setText(data['venue'])

            # Check if 'schedule' key exists in data before accessing it
            if 'result' in data and data['result']:
                self.resultbox.setCurrentText(data['result'])

            os.remove('clip.bin')

            

        except Exception as e:
            print(str(e))
            self.close()
        
        self.buttonBox.accepted.connect(self.create_json)
        self.buttonBox.rejected.connect(self.reject)

    def create_json(self):
        data = {
            'shortname': self.company.text(),
            'category': self.catbox.text(),
            'rollno': self.roll.text(),
            'extype': self.exambox.currentText(),
            'exdate': self.exdate.date().toString(Qt.ISODate),
            'venue': self.venue.text(),
            'result': self.resultbox.currentText()
        }

        with open('clip.bin', 'w') as file:
            json.dump(data, file, indent=4)

        self.accept()

class NewAppDiag (QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loadUi('src/ui/nadialog.ui',self)
        try:
            with open('clip.bin', 'r') as file:
                data = json.load(file)
            os.remove('clip.bin')
            self.company.setText(data['shortname'])
            self.designation.setText(data['designation'])
            if 'appdate' in data:
                self.appdate.setDate(QDate.fromString(data['appdate'], Qt.ISODate))
            else:
                self.appdate.setDate(QDate.currentDate())
            # Check if 'category' key exists in data before accessing it
            if 'category' in data and data['category']:
                self.catbox.setCurrentText(data['category'])

            # Check if 'regno' key exists in data before accessing it
            if 'regno' in data and data['regno']:
                self.regNo.setText(data['regno'])

            # Check if 'note' key exists in data before accessing it
            if 'note' in data and data['note']:
                self.note.setText(data['note'])

            # Check if 'schedule' key exists in data before accessing it
            if 'schedule' in data and data['schedule']:
                self.shedbox.setCurrentText(data['schedule'])
                if data['schedule'] == 'Yes':
                    self.shedbox.setEnabled(1)

            

        except Exception as e:
            print(str(e))
            self.close()
        
        self.buttonBox.accepted.connect(self.create_json)
        self.buttonBox.rejected.connect(self.reject)

    def create_json(self):
        data = {
            'shortname': self.company.text(),
            'category': self.catbox.currentText(),
            'designation': self.designation.text(),
            'appdate': self.appdate.date().toString(Qt.ISODate),
            'regno': self.regNo.text(),
            'note': self.note.text(),
            'schedule': self.shedbox.currentText()
        }

        with open('clip.bin', 'w') as file:
            json.dump(data, file, indent=4)
        

class NewCircDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loadUi('src/ui/ncdialog.ui',self)
        if os.path.exists('clip.bin'):            
            with open('clip.bin', 'r') as file:
                data = json.load(file)
            os.remove('clip.bin')
            self.fullname.setText(data['fullname'])
            self.shortname.setText(data['shortname'])
            self.designation.setText(data['designation'])
            self.appfee.setText(str(data['appfee']))
            self.lastdate.setDate(QDate.fromString(data['lastdate'], Qt.ISODate))
            self.appdate.setDate(QDate.fromString(data['startdate'], Qt.ISODate))
            self.statusbox.setCurrentText(data['status'])
            if data['status'] == 'Applied':
                self.statusbox.setEnabled(1)
        else:
            self.appdate.setDate(QDate.currentDate())
            self.lastdate.setDate(QDate.currentDate())

        self.buttonBox.accepted.connect(self.create_json)
        self.buttonBox.rejected.connect(self.reject)


    def create_json(self):
        data = {
            'fullname': self.fullname.text(),
            'shortname': self.shortname.text(),
            'designation': self.designation.text(),
            'appfee': self.appfee.text(),
            'startdate': self.appdate.date().toString(Qt.ISODate),
            'lastdate': self.lastdate.date().toString(Qt.ISODate),
            'status': self.statusbox.currentText()
        }

        with open('clip.bin', 'w') as file:
            json.dump(data, file, indent=4)


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About Job Application Manager")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Software Information
        software_info = QLabel("Job Application Manager\n\nVersion: 1.0\n\n"
                               "This is a specialized software for managing job applications "
                               "specifically tailored for Bangladesh government jobs. This software "
                               "efficiently records, tracks, and manages all job applications, providing "
                               "users with a centralized platform for easy monitoring and organization.")
        software_info.setWordWrap(True)

        layout.addWidget(software_info)

        # Contact Information
        contact_info = QLabel("\nContact:\n\n"
                              "Salman Mahmood Shovon\n"
                              "Phone: +8801753 999 841\n"
                              "Email: salman.eee@yahoo.com")

        layout.addWidget(contact_info)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        layout.addWidget(close_button)
        self.setLayout(layout)

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Job Application Manager Help")
        self.setFixedSize(990, 650)

        layout = QVBoxLayout()

        html_content ='''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><title>Job Application Manager Help Document</title><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\2610"; }
li.checked::marker { content: "\2612"; }
</style></head><body style=" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;">
<h1 style=" margin-top:20px; margin-bottom:10px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:xx-large; font-weight:700;">Job Application Manager Help Document </span></h1>
<h2 style=" margin-top:16px; margin-bottom:8px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;">Overview: </span></h2>
<p style=" margin-top:12px; margin-bottom:10px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif';">The Job Application Manager software is designed to streamline the management of government job applications and circulars. It provides a structured workflow to handle application statuses, examinations, results, and archiving. </span></p>
<h2 style=" margin-top:16px; margin-bottom:8px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;">Workflow: </span></h2>
<ol style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:12px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Enlist a Circular:</span> 
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">Provide details such as Organization Name, Short Name, Post Name, Application Fee, Application Start Date, Last Date, and Status (Applied or Pending). </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">If a circular is pending and its last date has expired, it will automatically move to the archive. </li></ul></li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Applications Data:</span> 
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">For applied circulars, additional information is required: </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">Application Date, Registration Number, Category (General or Technical), and Notes. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">Mark if scheduled for an exam. If not scheduled, it remains in the applications table. </li></ul></li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Exam Table:</span> 
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">When an exam is scheduled (marked as 'Yes' in the applications), it moves to the Exam table. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">Input Exam Date, Roll Number, Venue, Exam Type (MCQ, Written, Viva), and set the result to 'Pending' by default. </li></ul></li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:12px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Updating Results:</span> 
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">After the exam, when the result is published, modify the result in the Exam data. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">If the result is 'Passed,' the software will prompt whether it was the final stage. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">If it was the last stage, it moves to the Archive. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:140px; margin-right:120px; -qt-block-indent:0; text-indent:0px; line-height:160%;">If not the last stage, it prompts for details about the next exam date, type, and venue. </li></ul></li></ol>
<h2 style=" margin-top:16px; margin-bottom:8px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;">Software Features: </span></h2>
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:12px; margin-bottom:0px; margin-left:40px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Circular Management:</span> Create and manage circulars by providing essential details. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:40px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Application Tracking:</span> Track applied and pending applications with additional information like application date, registration number, category, notes, and scheduling for exams. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:12px; margin-left:40px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Exam Scheduling and Results:</span> Schedule exams for applications and input exam-related data (date, venue, type). Update exam results and manage subsequent stages based on the result (move to the archive or plan next stages). </li></ul>
<h2 style=" margin-top:16px; margin-bottom:8px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;">Usage Guide: </span></h2>
<ol style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:12px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Circular Enlistment:</span> Use the &quot;Circulars&quot; section to input details about available job circulars. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Application Tracking:</span> In the &quot;Applications&quot; section, manage applied and pending applications, inputting necessary details. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Exam Management:</span> Schedule exams by marking 'Yes' in the application details, then manage exam-related data in the &quot;Exams&quot; section. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Result Update and Progression:</span> Update exam results, and based on the outcome, decide on the progression of the application stage. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:12px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Archiving:</span> Access archived applications via the Menubar's Tool &gt; Archive option. </li></ol>
<h2 style=" margin-top:16px; margin-bottom:8px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;">Benefits: </span></h2>
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:12px; margin-bottom:0px; margin-left:40px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Efficient Tracking:</span> Track the entire application process from submission to final stages. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:0px; margin-left:40px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Structured Workflow:</span> Follow a structured workflow for exams, results, and subsequent stages. </li>
<li style=" font-family:'Arial','sans-serif';" style=" margin-top:0px; margin-bottom:12px; margin-left:40px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-weight:700;">Centralized Information:</span> Keep all application-related information organized and easily accessible. </li></ul>
<h2 style=" margin-top:16px; margin-bottom:8px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif'; font-size:x-large; font-weight:700;">More Help and Suggestion: </span></h2>
<p style=" margin-top:12px; margin-bottom:10px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif';">For further assistance and suggestion feel free to contact me: </span></p>
<p style=" margin-top:12px; margin-bottom:10px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif';">Salman Mahmood Shovon </span></p>
<p style=" margin-top:12px; margin-bottom:10px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif';">Phone: +8801753 999 841 </span></p>
<p style=" margin-top:12px; margin-bottom:10px; margin-left:20px; margin-right:20px; -qt-block-indent:0; text-indent:0px; line-height:160%;"><span style=" font-family:'Arial','sans-serif';">email: salman.eee@yahoo.com </span></p></body></html>
'''

        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml(html_content)
        layout.addWidget(text_browser)

        button_layout = QHBoxLayout()

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    icon = QIcon("src/assets/logo.ico") 
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec_())