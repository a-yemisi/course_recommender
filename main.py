import mysql.connector
import webbrowser
import sys
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow, QTableWidget, QHeaderView, QTableWidgetItem
import mysql.connector

#Connecting to the sql
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="2807",
  port =3306,
  database = "course_recommnder"
)
print(dataBase)

cur = dataBase.cursor()

#This is list of data needed for the interface, and gotten from the interface.
#They will be manipulated later in the code.
listt = ["---Please Choose---", "Mathematics", "F. Maths", "Physics", "Chemistry", "Biology", "Agriculture", "Lit. in English", "Hausa", "Igbo", "Yoruba", "Clothing and Textiles", "Visual Arts",
                  "Government", "Economics", "Geography", "CRS", "Islamic Studies", "Accounting", "Secretarial Duties", "Office Practice", "Book keeping", "Social Studies", "Statistics",
                 "Commerce", "Music", "Fine Arts", "Marketing", "Arabic", "History", "French", "Home Econs", "Shorthand", "Business method", "Integrated Science", "Fisheries", "Animal Husbandry",
                 "Computer Studies", "Food & Nut", "Technical Drawing", "Health and Physical Education", "Zoology", "Botany", "Edo", "Efik"]
forremoval = ["---Please Choose---", "Mathematics", "F. Maths", "Physics", "Chemistry", "Biology", "Agriculture", "Lit. in English", "Hausa", "Igbo", "Yoruba", "Clothing and Textiles", "Visual Arts",
                  "Government", "Economics", "Geography", "CRS", "Islamic Studies", "Accounting", "Secretarial Duties", "Office Practice", "Book keeping", "Social Studies", "Statistics",
                 "Commerce", "Music", "Fine Arts", "Marketing", "Arabic", "History", "French", "Home Econs", "Shorthand", "Business method", "Integrated Science", "Fisheries", "Animal Husbandry",
                 "Computer Studies", "Food & Nut", "Technical Drawing", "Health and Physical Education", "Zoology", "Botany", "Edo", "Efik"]
statelist = ["---Please Choose---", "All", "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta", "Ebonyi",
             "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi",
             "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto",
             "Taraba", "Yobe", "Zamfara"]
sciencesub = ["Biology", "Physics", "Chemistry", "F. Mathematics", "Health and Physical Education", "Computer Studies", "Agriculture", "Technical Drawing", "Food & Nut", "Geography"
              "Botany", "Zoology", "Geography"]
artsub = ["Lit. in English", "Fine Arts", "CRS", "Islamic Studies", "French", "Igbo", "Yoruba", "Hausa", "Arabic", "Music", "History", "Edo", "Efik"]
socialscicub = ["Economics", "Government", "Geography", "Accounting", "Commerce", "Marketing"]

# Sorting out O'level subject list
listt.sort();   forremoval.sort()

# Creating lists for selected faculty, subjects, and grades of the Prospective candidates
selectedfac = [];   selectedsub = [];   selectedgra = [];   name =[]

# Lists to store details about recommended universities and their properties
courseID = [];  course_name = [];   uni_name = [];  uni_state = [];     uni_site = [];      course_ID = [];     req = [];   rowlim = [0];   sortby = []


# First Screen loaded from UI
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("frontpage.ui", self)
        self.qcontinue.clicked.connect(self.gotoinsert)
    def gotoinsert(self):

        # Clearing previous data
        selectedsub.clear()
        selectedfac.clear()
        selectedgra.clear()

        # Ensuring name is filled
        text = self.lineEdit.text()
        if text == "":
            self.nameError.setText("*Please Enter your name*")
        else:
            tocaptal = text[0].upper() + text[1:]
            print(tocaptal)
            name.clear()
            name.append(tocaptal)
            insert = insertscreen()
            widget.addWidget(insert)
            widget.setCurrentIndex(widget.currentIndex()+1)


# Insert Screen Class
class insertscreen(QMainWindow):
    def __init__(self):
        super(insertscreen, self).__init__()
        loadUi("insertpage.ui", self)
        self.toTweak.clicked.connect(self.gotoTweak)
        self.nextTweak.clicked.connect(self.gotoTweak)
        # self.toDisplay.clicked.connect(self.gotoFinal)
        self.backtoinsert.clicked.connect(self.toInsert)

        # Getting values to combo boxes
        self.suba.addItem("English Language")
        for x in listt:
            self.subb.addItem(x)
        for x in listt:
            self.subc.addItem(x)
        for x in listt:
            self.subd.addItem(x)
        for x in listt:
            self.sube.addItem(x)
        cur.execute("SELECT faculty_name FROM faculty_list;")
        fetched = cur.fetchall()
        self.facul.addItem("---Please Choose---")
        self.facul.addItem("All")
        for i in fetched:
            tostr = i[0]
            self.facul.addItem(tostr)

        # Adding already selected values to show up
        if len(selectedsub) == 0:
            pass
        else:
            self.suba.setCurrentText(selectedsub[0])
            self.subb.setCurrentText(selectedsub[1])
            self.subc.setCurrentText(selectedsub[2])
            self.subd.setCurrentText(selectedsub[3])
            self.sube.setCurrentText(selectedsub[4])

        if len(selectedfac) == 0:
            pass
        else:
            self.facul.setCurrentText(selectedfac[0])

        #Activating editing the values of the combo boxes
        self.subb.activated.connect(self.printoutb)
        self.subc.activated.connect(self.printoutc)
        self.subd.activated.connect(self.printoutd)

    def printoutb(self):
        newlist = []
        current = self.subb.currentText()
        for i in forremoval:
            if current == i and current != "---Please Choose---":
                pass
            else:
                newlist.append(i)
        #changinglist.append(current)
        self.subc.clear()
        self.subd.clear()
        self.sube.clear()
        for j in newlist:
            self.subc.addItem(j)
            self.subd.addItem(j)
            self.sube.addItem(j)

    def printoutc(self):
        newlist = []
        current = self.subc.currentText()
        for i in forremoval:
            if current == i and current != "---Please Choose---":
                pass
            elif self.subb.currentText() == i and self.subb.currentText() != "---Please Choose---":
                pass
            else:
                newlist.append(i)
        self.subd.clear()
        self.sube.clear()
        for j in newlist:
            self.subd.addItem(j)
            self.sube.addItem(j)

    def printoutd(self):
        newlist = []
        current = self.subd.currentText()
        for i in forremoval:
            if current == i and current != "---Please Choose---":
                pass
            elif self.subb.currentText() == i and self.subb.currentText() != "---Please Choose---":
                pass
            elif self.subc.currentText() == i and self.subc.currentText() != "---Please Choose---":
                pass
            else:
                newlist.append(i)
        self.sube.clear()
        for j in newlist:
            self.sube.addItem(j)



    def toInsert(self):
        insert = insertscreen()
        widget.addWidget(insert)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoTweak(self):

        #Getting column value for selectedsub
        selectedsub.clear()
        selectedsub.append(self.suba.currentText())
        selectedsub.append(self.subb.currentText())
        selectedsub.append(self.subc.currentText())
        selectedsub.append(self.subd.currentText())
        selectedsub.append(self.sube.currentText())

        #Getting combo box value for selected faculty
        selectedfac.clear()
        selectedfac.append(self.facul.currentText())

        k = 0
        while k < len(selectedsub):
            if selectedsub[k] == "---Please Choose---":
                selectedsub[k] = "NULL"
            else:
                pass
            k = k + 1

        l = 0
        while l < len(selectedfac):
            if selectedfac[l] == "---Please Choose---":
                selectedfac[l] = "All"
            else:
                pass
            l = l + 1

        # Getting grades from Radio button
        selectedgra.clear()
        ##For Subject A:
        if self.sub1A1.isChecked():
            selectedgra.append("A1")
        elif self.sub1B2.isChecked():
            selectedgra.append("B2")
        elif self.sub1B3.isChecked():
            selectedgra.append("B3")
        elif self.sub1C4.isChecked():
            selectedgra.append("C4")
        elif self.sub1C5.isChecked():
            selectedgra.append("C5")
        elif self.sub1C6.isChecked():
            selectedgra.append("C6")
        elif self.sub1D7.isChecked():
            selectedgra.append("D7")
        elif self.sub1E8.isChecked():
            selectedgra.append("E8")
        elif self.sub1F9.isChecked():
            selectedgra.append("F9")
        elif self.sub1AR.isChecked():
            selectedgra.append("AR")
        else: selectedgra.append("AR")

        ##For Subject B:
        if self.sub2A1.isChecked():
            selectedgra.append("A1")
        elif self.sub2B2.isChecked():
            selectedgra.append("B2")
        elif self.sub2B3.isChecked():
            selectedgra.append("B3")
        elif self.sub2C4.isChecked():
            selectedgra.append("C4")
        elif self.sub2C5.isChecked():
            selectedgra.append("C5")
        elif self.sub2C6.isChecked():
            selectedgra.append("C6")
        elif self.sub2D7.isChecked():
            selectedgra.append("D7")
        elif self.sub2E8.isChecked():
            selectedgra.append("E8")
        elif self.sub2F9.isChecked():
            selectedgra.append("F9")
        elif self.sub2AR.isChecked():
            selectedgra.append("AR")
        else:
            selectedgra.append("AR")

        ##For Subject C:
        if self.sub3A1.isChecked():
            selectedgra.append("A1")
        elif self.sub3B2.isChecked():
            selectedgra.append("B2")
        elif self.sub3B3.isChecked():
            selectedgra.append("B3")
        elif self.sub3C4.isChecked():
            selectedgra.append("C4")
        elif self.sub3C5.isChecked():
            selectedgra.append("C5")
        elif self.sub3C6.isChecked():
            selectedgra.append("C6")
        elif self.sub3D7.isChecked():
            selectedgra.append("D7")
        elif self.sub3E8.isChecked():
            selectedgra.append("E8")
        elif self.sub3F9.isChecked():
            selectedgra.append("F9")
        elif self.sub3AR.isChecked():
            selectedgra.append("AR")
        else:
            selectedgra.append("AR")

        ##For Subject D:
        if self.sub4A1.isChecked():
            selectedgra.append("A1")
        elif self.sub4B2.isChecked():
            selectedgra.append("B2")
        elif self.sub4B3.isChecked():
            selectedgra.append("B3")
        elif self.sub4C4.isChecked():
            selectedgra.append("C4")
        elif self.sub4C5.isChecked():
            selectedgra.append("C5")
        elif self.sub4C6.isChecked():
            selectedgra.append("C6")
        elif self.sub4D7.isChecked():
            selectedgra.append("D7")
        elif self.sub4E8.isChecked():
            selectedgra.append("E8")
        elif self.sub4F9.isChecked():
            selectedgra.append("F9")
        elif self.sub4AR.isChecked():
            selectedgra.append("AR")
        else:
            selectedgra.append("AR")

        ##For Subject E:
        if self.sub5A1.isChecked():
            selectedgra.append("A1")
        elif self.sub5B2.isChecked():
            selectedgra.append("B2")
        elif self.sub5B3.isChecked():
            selectedgra.append("B3")
        elif self.sub5C4.isChecked():
            selectedgra.append("C4")
        elif self.sub5C5.isChecked():
            selectedgra.append("C5")
        elif self.sub5C6.isChecked():
            selectedgra.append("C6")
        elif self.sub5D7.isChecked():
            selectedgra.append("D7")
        elif self.sub5E8.isChecked():
            selectedgra.append("E8")
        elif self.sub5F9.isChecked():
            selectedgra.append("F9")
        elif self.sub5AR.isChecked():
            selectedgra.append("AR")
        else:
            selectedgra.append("AR")

        print("Hiii " + name[0] + "!")
        print("Faculty selected is: " + selectedfac[0])

        print("These are the grades you got for each subject")
        j = 0
        while j < 5:
            print(selectedsub[j] + ": " + selectedgra[j])
            j = j + 1

        #Forcing the user to input result:
        if selectedsub[1] == "NULL" or selectedsub[1] == "NULL" or selectedsub[2] == "NULL" or selectedsub[3] == "NULL":
            self.warning.clear()
            self.warning.setText("*Not all subjects have been selected*")
        else:
            tweak = tweakpage()
            widget.addWidget(tweak)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class tweakpage(QMainWindow):
    def __init__(self):
        super(tweakpage, self).__init__()
        loadUi("tweakpage.ui", self)
        self.tofinalt.clicked.connect(self.toFinal)
        self.toinsertt.clicked.connect(self.gotoInsert)

        # Setting the table widget size
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #Opening the link
        self.tableWidget.itemDoubleClicked.connect(self.OpennLink)

        #Add value to faculty column box
        cur.execute("SELECT faculty_name FROM faculty_list;")
        fetched = cur.fetchall()
        self.tweakFac.addItem("---Please Choose---")
        self.tweakFac.addItem("All")
        for i in fetched:
            tostr = i[0]
            self.tweakFac.addItem(tostr)
        item = selectedfac[0]
        self.tweakFac.setCurrentText(item)

        #Add value to state column box
        for i in statelist:
            if i == "---Please Choose---" or i == "All":
                self.tweakState.addItem(i)
            else:
                toadd = i + " State"
                self.tweakState.addItem(toadd)

        # Adding the initial uniilist to the combobox
        self.tweakName.clear()
        self.tweakName.addItem("---Please Choose---")
        self.tweakName.addItem("All")
        cur.execute("SELECT uni_name FROM universities")
        resultuni = cur.fetchall()
        for i in resultuni:
            tostr = i[0]
            self.tweakName.addItem(tostr)

        # Making the university type combo box react with the University Name Combo box
        self.tweakType.activated.connect(self.reacttype)
        self.tweakState.activated.connect(self.reacttype)
        self.showTweak.clicked.connect(self.go)
        self.nextPage.clicked.connect(self.toFinal)


    # Trying to ensure that the name that comes up as Uni name matches type and State
    def reacttype(self):
        if self.tweakState.currentText() == "---Please Choose---" or self.tweakState.currentText() == "All":
            if self.tweakType.currentText() == "---Please Choose---" or self.tweakType.currentText() == "All":
                cur.execute("SELECT uni_name FROM universities")
                result = cur.fetchall()
                self.tweakName.clear()
                self.tweakName.addItem("---Please Choose---")
                self.tweakName.addItem("All")
                for i in result:
                    tostr = i[0]
                    self.tweakName.addItem(tostr)
            else:
                typevalue = self.tweakType.currentText()
                toexecute = "SELECT uni_name FROM universities WHERE uni_type = '" + typevalue + "'"
                cur.execute(toexecute)
                result = cur.fetchall()
                self.tweakName.clear()
                self.tweakName.addItem("---Please Choose---")
                self.tweakName.addItem("All")
                for i in result:
                    tostr = i[0]
                    self.tweakName.addItem(tostr)
        else:
            statevalue = self.tweakState.currentText()
            typevalue = self.tweakType.currentText()
            if typevalue == "All" or typevalue == "---Please Choose---":
                toexec = "SELECT uni_name FROM universities WHERE uni_state = '"
                statevalue = statevalue + "'"
                execute = toexec + statevalue
                cur.execute(execute)
                result = cur.fetchall()
                self.tweakName.clear()
                self.tweakName.addItem("---Please Choose---")
                self.tweakName.addItem("All")
                for i in result:
                    tostr = i[0]
                    self.tweakName.addItem(tostr)
            else:
                toexec = "SELECT uni_name FROM universities WHERE uni_state = '"
                execute = toexec + statevalue + "' " + "and uni_type = '" + typevalue + "'"
                cur.execute(execute)
                result = cur.fetchall()
                self.tweakName.clear()
                self.tweakName.addItem("---Please Choose---")
                self.tweakName.addItem("All")
                for i in result:
                    tostr = i[0]
                    self.tweakName.addItem(tostr)

    def go(self):
        #Forming the Query Statement for the sql
        baseexec = "SELECT courseID FROM req_olevel, universities WHERE uniID_offering = uniID"
        courseID.clear();   course_name.clear();    uni_name.clear();   uni_state.clear();  uni_site.clear();   course_ID.clear();   req.clear()
        cat1 = []
        cat2 = []

        # Making the table empty
        self.tableWidget.setRowCount(0)

        #Forming list based on a type category
        for i in selectedsub:
            if i in socialscicub:
                cat1.append("Social Science subject")
            elif i in artsub:
                cat1.append("Art subject")
            elif i in sciencesub:
                cat1.append("Science subject")
            else:
                cat1.append(" ")
        #Forming list based on two types category
        for i in selectedsub:
            if i in socialscicub or i in artsub:
                cat2.append("Art / Social Science subject")
            elif i in socialscicub or i in sciencesub:
                cat2.append("Science / Social Science subject")
            else:
                cat2.append(" ")


        #Adding tweaking values
        #Faculty
        faculty = self.tweakFac.currentText()
        unicase = []
        if faculty == "---Please Choose---" or faculty == "All":
            unicase.append(" ")
        else:
            unicase.append(" and course_faculty = '" + faculty + "'")

        #UniType
        unitype = self.tweakType.currentText()
        if unitype == "---Please Choose---" or unitype == "All":
            unicase.append(" ")
        else:
            unicase.append(" and uni_type = '" + unitype + "'")

        #UniState
        unistate = self.tweakState.currentText()
        if unistate == "---Please Choose---" or unistate == "All":
            unicase.append(" ")
        else:
            unicase.append(" and uni_state = '" + unistate + "'")

        #UniName
        uniname = self.tweakName.currentText()
        if uniname == "---Please Choose---" or uniname == "All":
            unicase.append(" ")
        else:
            unicase.append(" and uni_name = '" + uniname + "'")

        baseexec = baseexec + unicase[0] + unicase[1] + unicase[2] + unicase[3]


        #Declaring the columns as lists. Subjects are elements in the list
        colma = "";     colm = []
        subs = ["subB", "subC", "subD", "subE"]

        #This is for turning the selected grades into something that can be processed by the db
        forsql = []
        p = 0
        while p < len(selectedgra):
            if selectedgra[p] == 'A1' or selectedgra[p] == 'B2' or selectedgra[p] == 'B3' or selectedgra[p] == 'C4' or \
                    selectedgra[p] == 'C5' or selectedgra[p] == 'C6':
                forsql.append("C6")
            else:
                forsql.append(selectedgra[p])
            p = p + 1

        #Subject and Column A
        if forsql[0] == "AR" or forsql[0] == "C6":
            pass
        else:
            colma = " and subA_lowestgrade = '" + forsql[0] + "'"

    #Column B to E
        q = 1
        # Column B - E
        for i in subs:
            while (q < 5):
                if forsql[q] == "AR":
                    colm.append("(olevel_" + i + " like '%" + selectedsub[q] + "%')")
                else:
                    colm.append(
                        "(olevel_" + i + " like '%" + selectedsub[q] + "%' and " + i + "_lowestgrade = '" + forsql[q] + "')")
                q = q + 1
            q = 1

        def output():
            boutput = "(" + colm[0] + " or " + colm[1] + " or " + colm[2] + " or " + colm[3] + ")"
            coutput = "(" + colm[4] + " or " + colm[5] + " or " + colm[6] + " or " + colm[7] + ")"
            doutput = "(" + colm[8] + " or " + colm[9] + " or " + colm[10] + " or " + colm[11] + ")"
            eoutput = "(" + colm[12] + " or " + colm[13] + " or " + colm[14] + " or " + colm[15] + ")"
            allsub = boutput + " and " + coutput + " and " + doutput + " and " + eoutput
            finall =  baseexec + colma + " and " + allsub
            return finall
        #Printing first Query Result
        toexec = output()
        cur.execute(toexec)
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        #Executing the query with category on column E:
        def findknown1(x, y, z):
            colm.clear()
            m = 0
            indexlist = []
            indexlist.append(x);    indexlist.append(y);    indexlist.append(z)
            while (m < 3):
                for j in indexlist:
                    if forsql[j] == "AR" or forsql[j] == "C6":
                        colm.append("(olevel_" + subs[m] + " like '%" + selectedsub[j] + "%')")
                    else:
                        colm.append(
                            "(olevel_" + subs[m] + " like '%" + selectedsub[j] + "%' and " + subs[m] + "_lowestgrade = '" +
                            forsql[j] + "')")
                m += 1
        # Bringing them together
        def threeksubp():
            boutput = "(" + colm[0] + " or " + colm[1] + " or " + colm[2] + ")"
            coutput = "(" + colm[3] + " or " + colm[4] + " or " + colm[5] + ")"
            doutput = "(" + colm[6] + " or " + colm[7] + " or " + colm[8] + ")"
            eoutput = colm[9]
            allsub = boutput + " and " + coutput + " and " + doutput + " and " + eoutput
            finall = baseexec + colma + " and " + allsub
            return finall

        # Sub BCD, cat1 E
        findknown1(1,2,3)
        # Column E
        if forsql[4] =="AR" or forsql[4] == "C6":
            colm.append("(olevel_subE = '" + cat1[4] + "')")
        else:
            colm.append("(olevel_subE = '" + cat1[4] + "' and " + "subE_lowestgrade = '" + forsql[4] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BCD, cat2 E
        findknown1(1,2,3)
        # Column E
        if forsql[4] == "AR" or forsql[4] == "C6":
            colm.append("(olevel_subE = '" + cat2[4] + "')")
        else:
            colm.append("(olevel_subE = '" + cat2[4] + "' and " + "subE_lowestgrade = '" + forsql[4] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BCD, All E
        findknown1(1, 2, 3)
        # Column E
        if forsql[4] == "AR" or forsql[4] == "C6":
            colm.append("(olevel_subE = 'all')")
        else:
            colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[4] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BDE, cat1 C
        findknown1(1,3,4)
        # Column E
        if forsql[2] == "AR" or forsql[2] == "C6":
            colm.append("(olevel_subE = '" + cat1[2] + "')")
        else:
            colm.append("(olevel_subE = '" + cat1[2] + "' and " + "subE_lowestgrade = '" + forsql[2] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BDE cat2 C
        findknown1(1,3,4)
        # Column E
        if forsql[2] == "AR" or forsql[2] == "C6":
            colm.append("(olevel_subE = '" + cat2[2] + "')")
        else:
            colm.append("(olevel_subE = '" + cat2[2] + "' and " + "subE_lowestgrade = '" + forsql[2] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BDE, All C
        findknown1(1,3,4)
        # Column E
        if forsql[2] == "AR" or forsql[2] == "C6":
            colm.append("(olevel_subE = 'all')")
        else:
            colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[2] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub CDE cat1 B
        findknown1(2,3,4)
        # Column E
        if forsql[1] == "AR" or forsql[1] == "C6":
            colm.append("(olevel_subE = '" + cat1[1] + "')")
        else:
            colm.append("(olevel_subE = '" + cat1[1] + "' and " + "subE_lowestgrade = '" + forsql[1] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub CDE cat2 B
        findknown1(2,3,4)
        # Column E
        if forsql[1] == "AR" or forsql[1] == "C6":
            colm.append("(olevel_subE = '" + cat2[1] + "')")
        else:
            colm.append("(olevel_subE = '" + cat2[1] + "' and " + "subE_lowestgrade = '" + forsql[1] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub CDE, All B
        findknown1(2,3,4)
        # Column E
        if forsql[1] == "AR" or forsql[1] == "C6":
            colm.append("(olevel_subE = 'all')")
        else:
            colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[1] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BCE cat1 D
        findknown1(1,2,4)
        # Column E
        if forsql[3] == "AR" or forsql[3] == "C6":
            colm.append("(olevel_subE = '" + cat1[3] + "')")
        else:
            colm.append("(olevel_subE = '" + cat1[3] + "' and " + "subE_lowestgrade = '" + forsql[3] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BCE cat2 D
        findknown1(1,2,4)
        # Column E
        if forsql[3] == "AR" or forsql[3] == "C6":
            colm.append("(olevel_subE = '" + cat2[3] + "')")
        else:
            colm.append("(olevel_subE = '" + cat2[3] + "' and " + "subE_lowestgrade = '" + forsql[3] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # Sub BCD, All D
        findknown1(1, 2, 4)
        # Column E
        if forsql[3] == "AR" or forsql[3] == "C6":
            colm.append("(olevel_subE = 'all')")
        else:
            colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[3] + "')")
        cur.execute(threeksubp())
        result = cur.fetchall()
        for i in result:
            course_ID.append(i[0])

        # a in the function is index of the first known subject   # b is the is index of second
        # x is the is index of category subject1         # x is the is index of second

        # Executing the Query with category on column D and E:
        # This is the function
        def twoknown(a,b,x,y):

            # D: Cat1 sub1, E: cat1 sub2
            indexxlist = [a, b]

            def findknown():
                colm.clear()
                m = 0
                while (m < 2):
                    for j in indexxlist:
                        if forsql[j] == "AR" or forsql[j] == "C6":
                            colm.append("(olevel_" + subs[m] + " like '%" + selectedsub[j] + "%')")
                        else:
                            colm.append(
                                "(olevel_" + subs[m] + " like '%" + selectedsub[j] + "%' and " + subs[


                                    m] + "_lowestgrade = '" +
                                forsql[j] + "')")
                    m += 1

            def twoksubp():
                boutput = "(" + colm[0] + " or " + colm[1] + ")"
                coutput = "(" + colm[2] + " or " + colm[3] + ")"
                doutput = colm[4]
                eoutput = colm[5]
                allsub = boutput + " and " + coutput + " and " + doutput + " and " + eoutput
                finall = baseexec + colma + " and " + allsub
                return finall

            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = '" + cat1[x] + "')")
            else:
                colm.append("(olevel_subD = '" + cat1[x] + "' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subE = '" + cat1[y] + "')")
            else:
                colm.append("(olevel_subE = '" + cat1[y] + "' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat2 sub1, E: cat2 sub2
            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = '" + cat2[x] + "')")
            else:
                colm.append("(olevel_subD = '" + cat2[x] + "' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subE = '" + cat2[y] + "')")
            else:
                colm.append("(olevel_subE = '" + cat2[y] + "' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat1 sub1, E: cat2 sub2
            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = '" + cat1[x] + "')")
            else:
                colm.append("(olevel_subD = '" + cat1[x] + "' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subE = '" + cat2[y] + "')")
            else:
                colm.append("(olevel_subE = '" + cat2[y] + "' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat2 sub1, E: cat1 sub2
            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = '" + cat2[x] + "')")
            else:
                colm.append("(olevel_subD = '" + cat2[x] + "' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subE = '" + cat1[y] + "')")
            else:
                colm.append("(olevel_subE = '" + cat1[y] + "' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat1 sub2, E: cat1 sub1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = '" + cat1[y] + "')")
            else:
                colm.append("(olevel_subD = '" + cat1[y] + "' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = '" + cat1[x] + "')")
            else:
                colm.append("(olevel_subE = '" + cat1[x] + "' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat2 sub2 E: cat2 sub1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = '" + cat2[y] + "')")
            else:
                colm.append("(olevel_subD = '" + cat2[y] + "' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = '" + cat2[x] + "')")
            else:
                colm.append("(olevel_subE = '" + cat2[x] + "' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat1 sub2, E: Cat2 sub1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = '" + cat1[y] + "')")
            else:
                colm.append("(olevel_subD = '" + cat1[y] + "' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = '" + cat2[x] + "')")
            else:
                colm.append("(olevel_subE = '" + cat2[x] + "' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat 2 sub2, E: cat1 sub1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = '" + cat2[y] + "')")
            else:
                colm.append("(olevel_subD = '" + cat2[y] + "' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = '" + cat1[x] + "')")
            else:
                colm.append("(olevel_subE = '" + cat1[x] + "' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: All, known grades for unknown subject1, E: All, known grades for unknown subject2
            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = 'all')")
            else:
                colm.append("(olevel_subD = 'all' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR"or forsql[y] == "C6":
                colm.append("(olevel_subE = 'all')")
            else:
                colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: All, known grades for unknown subject2, E: All, known grades for unknown subject1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = 'all')")
            else:
                colm.append("(olevel_subD = 'all' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = 'all')")
            else:
                colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat1, sub 1; E: All, known grades for unknown subject 2
            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = '" + cat1[x] + "')")
            else:
                colm.append("(olevel_subD = '" + cat1[x] + "' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subE = 'all')")
            else:
                colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat2, sub 1; E: All, known grades for unknown subject 2
            # Column B & C
            findknown()
            # Column D
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subD = '" + cat2[x] + "')")
            else:
                colm.append("(olevel_subD = '" + cat2[x] + "' and " + "subD_lowestgrade = '" + forsql[x] + "')")
            # Column E
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subE = 'all')")
            else:
                colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[y] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat1, sub 2; E: All, known grades for unknown subject 1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = '" + cat1[y] + "')")
            else:
                colm.append("(olevel_subD = '" + cat1[y] + "' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = 'all')")
            else:
                colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

            # D: Cat2, sub 2; E: All, known grades for unknown subject 1
            # Column B & C
            findknown()
            # Column D
            if forsql[y] == "AR" or forsql[y] == "C6":
                colm.append("(olevel_subD = '" + cat2[y] + "')")
            else:
                colm.append("(olevel_subD = '" + cat2[y] + "' and " + "subD_lowestgrade = '" + forsql[y] + "')")
            # Column E
            if forsql[x] == "AR" or forsql[x] == "C6":
                colm.append("(olevel_subE = 'all')")
            else:
                colm.append("(olevel_subE = 'all' and " + "subE_lowestgrade = '" + forsql[x] + "')")
            cur.execute(twoksubp())
            result = cur.fetchall()
            for i in result:
                course_ID.append(i[0])

        #Running the function
        twoknown(1,2,3,4)
        twoknown(1,3,2,4)
        twoknown(2,3,1,4)
        twoknown(1,4,2,3)
        twoknown(2,4,1,3)
        twoknown(3,4,1,2)

        def oneknown(a, b, c, d):
            known = a





        # Done with Processing: Post Process
        # Removing duplicates
        for i in course_ID:
            if i not in courseID:
                courseID.append(i)

        for i in courseID:
            run = "SELECT course_name, uni_name, uni_site, uni_state FROM req_olevel, universities WHERE uniID_offering = uniID and instanceID = '1' and courseID = '" + str(i) + "'"
            cur.execute(run)
            result = cur.fetchall()
            for j in result:
                #print(j)
                course_name.append(j[0])
                uni_name.append(j[1])
                uni_site.append(j[2])
                uni_state.append(j[3])


        rowlimit = 0
        rowlim.clear()
        if len(course_name) == 0:
            rowlimit = 0
            rowlim.append(rowlimit)
        else:
            rowlimit = len(course_name)
            rowlim.append(rowlimit)


        # Getting Items to be added to the combo box
        for b in courseID:
            cur.execute("select jamb_subA, jamb_subB, jamb_subC, jamb_subD from req_utme where courseID = '" + str(b) + "'")
            resultt = cur.fetchall()
            for k in resultt:
                if k[2] == k[3]:
                    subjects =  k[0] + ", " + k[1] + " and two of " + k[2] + "."
                    req.append(subjects)
                elif k[1] == k[2]:
                    subjects = k[0] + ", any two of " + k[2] + ", and " + k[3] + "."
                    req.append(subjects)
                elif k[1] == k[2] and k[2] == k[3]:
                    subjects = k[1] + " and any three of " + k[2] + "."
                    req.append(subjects)
                else:
                    subjects = k[0] + ", " + k[1] + ", " + k[2] + " and " + k[3] + "."
                    req.append(subjects)

        sortby.clear()
        data = list(zip(course_name, uni_name, uni_site, uni_state))
        if self.courseN.isChecked():
            sortby.append("ByCourse")
            data.sort(key=lambda c: c[0], reverse=False)
            course_name.clear();
            uni_name.clear();
            uni_site.clear();
            uni_state.clear()
            for k in data:
                course_name.append(k[0])
                uni_name.append(k[1])
                uni_site.append(k[2])
                uni_state.append(k[3])
                #print(k)
        #    self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        else:
            sortby.append("ByUni")
            data.sort(key=lambda c: c[1], reverse=False)
            course_name.clear();
            uni_name.clear();
            uni_site.clear();
            uni_state.clear()
            for k in data:
                course_name.append(k[0])
                uni_name.append(k[1])
                uni_site.append(k[2])
                uni_state.append(k[3])
                #print(k)

        tablerow = 0
        # Adding Data to the table
        if rowlimit == 0:
            pass
            self.noData.setText("No Data")
            self.tableWidget.setRowCount(rowlimit)
        else:
            self.noData.clear()
            self.tableWidget.setRowCount(rowlimit)
            while tablerow < len(course_name):
                self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(course_name[tablerow]))
                self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(uni_name[tablerow]))
                self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(uni_site[tablerow]))
                self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(uni_state[tablerow]))
                self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(req[tablerow]))
                tablerow = tablerow + 1

        sortby.clear()
        data = list(zip(course_name, uni_name, uni_site, uni_state))
        if self.courseN.isChecked():
            sortby.append("ByCourse")
            data.sort(key=lambda c: c[0], reverse=False)
            course_name.clear();    uni_name.clear();   uni_site.clear();   uni_state.clear()
            for k in data:
                course_name.append(k[0])
                uni_name.append(k[1])
                uni_site.append(k[2])
                uni_state.append(k[3])
                print(k)
        #    self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        else:
            sortby.append("ByUni")
            data.sort(key=lambda c: c[1], reverse=False)
            course_name.clear();    uni_name.clear();   uni_site.clear();   uni_state.clear()
            for k in data:
                course_name.append(k[0])
                uni_name.append(k[1])
                uni_site.append(k[2])
                uni_state.append(k[3])
                print(k)





    def gotoInsert(self):
        insert = insertscreen()
        widget.addWidget(insert)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def toFinal(self):
        final = finalpage()
        widget.addWidget(final)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def OpennLink(self, item):
        if item.column() == 2:
            url = "http://" + item.text()
            webbrowser.open(url)



class finalpage(QMainWindow):
    def __init__(self):
        super(finalpage, self).__init__()
        loadUi("finalpage.ui", self)
        todis = name[0]
        towrite = "Hii " + todis + "!"
        self.displayName.setText(towrite)

        # Setting the table widget size
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Go to Insert
        self.toInsertF.clicked.connect(self.gottoInsert)
        self.toTweakF.clicked.connect(self.gottoTweak)
        self.qhome.clicked.connect(self.gohome)

        # Enabling function to open webbrowser
        self.tableWidget.itemDoubleClicked.connect(self.OpenLink)

        # Adding value to table

        tablerow = 0
        # Adding Data to the table
        rowlimit = rowlim[0]
        print(rowlimit)
        if rowlimit == 0:
            self.noData.setText("No Data")
            self.tableWidget.setRowCount(rowlimit)
        else:
            self.noData.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(rowlimit)
            while tablerow < len(course_name):
                self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(course_name[tablerow]))
                self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(uni_name[tablerow]))
                self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(uni_site[tablerow]))
                self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(uni_state[tablerow]))
                self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(req[tablerow]))
                tablerow = tablerow + 1

        if sortby[0] == "ByCourse":
            self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        elif sortby[0] == "ByUni":
            self.tableWidget.sortItems(1, QtCore.Qt.AscendingOrder)
        else:
            pass

    def OpenLink(self, item):
        if item.column() == 2:
            url = "http://" + item.text()
            webbrowser.open(url)

    def gottoInsert(self):
        insert = insertscreen()
        widget.addWidget(insert)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gottoTweak(self):
        tweak = tweakpage()
        widget.addWidget(tweak)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gohome(self):
        welcomee = WelcomeScreen()
        widget.addWidget(welcomee)
        widget.setCurrentIndex(widget.currentIndex() + 1)



app = QApplication(sys.argv)
welcome=WelcomeScreen()
widget = QtWidgets.QStackedWidget()

widget.addWidget((welcome))
widget.setFixedHeight(600)
widget.setFixedWidth(1000)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")