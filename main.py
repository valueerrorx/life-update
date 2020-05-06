#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from PyQt5 import QtCore, uic, QtWidgets

import subprocess
import threading
import time
import socket
from PyQt5.Qt import QIcon
from widget.SwitchButton import SwitchButton

USER = subprocess.check_output("logname", shell=True).rstrip().decode()
USER_HOME_DIR = os.path.join("/home", str(USER))
WORK_DIRECTORY = os.path.join(USER_HOME_DIR, ".life")


class Updater(threading.Thread):
    """ in order to provide a NONBLocking loop that 
    periodically checks the internet connection 
    this is done it a separate thread
    """
    def __init__(self, mainui):
        threading.Thread.__init__(self)
        self.mainui= mainui
        self.stop = False

    def run(self):
        while self.stop == False:
            self.update()
            time.sleep(5)
            
            
    def update(self):
        #update life EXAM
        line = "Updating LiFE Exam...\n"
 
        self.mainui.line = line
        self.mainui.updatesignal.emit()
    
        cmd = "cd %s/applications/life-exam && git pull " %(WORK_DIRECTORY)
        proc = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stderr.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        
        for line in iter(proc.stdout.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        proc.communicate()     
        
        time.sleep(1)



        #update life nextcloudusers
        line = "\nUpdating LiFE Nextcloudusers...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd %s/applications/life-nextcloudusers && git pull " %(WORK_DIRECTORY)
        proc1 = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc1.stderr.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        
        for line in iter(proc1.stdout.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        proc1.communicate() 
        
        
        time.sleep(1)   
        
        
        
        
        #update life UPDATE
        line = "\nUpdating LiFE Update...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd %s/applications/life-update && git pull " %(WORK_DIRECTORY)
        proc2 = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc2.stderr.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        
        for line in iter(proc2.stdout.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        proc2.communicate() 
        
        
        time.sleep(1)   
 
     
     
        #update life FIRSTSTART
        line = "\nUpdating LiFE Firststart...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd %s/applications/life-firststart && git pull " %(WORK_DIRECTORY)
        proc3 = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc3.stderr.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        
        for line in iter(proc3.stdout.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        proc3.communicate() 
        
        
        time.sleep(1)   
     
        
        #update life builder
        line = "\nUpdating LiFE Builder...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd %s/applications/life-builder && git pull " %(WORK_DIRECTORY)
        proc4 = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc4.stderr.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        
        for line in iter(proc4.stdout.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        proc4.communicate() 
        
        
        time.sleep(1)   
        
        
        #update life kiosk
        line = "\nUpdating LiFE Kiosk...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd %s/applications/life-kiosk && git pull " %(WORK_DIRECTORY)
        proc5 = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc5.stderr.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        
        for line in iter(proc5.stdout.readline, b''):
            if line:
                self.mainui.line = line.decode()
                self.mainui.updatesignal.emit()
        proc5.communicate() 
        
        
        time.sleep(1) 

        self.mainui.finishedsignal.emit()
        self.stop = True
  



class InetChecker(threading.Thread):
    """ in order to provide a NONBLocking loop that 
    periodically checks the internet connection 
    this is done it a separate thread
    """
    def __init__(self, mainui):
        threading.Thread.__init__(self)
        self.mainui = mainui

    def run(self):
        while self.mainui.check == True:
            time.sleep(5)
            self._checkOnline()

    def _checkOnline(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("github.com",80))
            s.close()
            if self.mainui.check == True:
                print ("online")
                self.mainui.onsignal.emit()
            return True
        except:
            print ("offline")     
            self.mainui.offsignal.emit()
            return False

class MeinDialog(QtWidgets.QDialog):
    # use signals and slots to talk between the UI dialog and the python thread otherwise it will throw warnings all over the place
    onsignal = QtCore.pyqtSignal()   
    offsignal = QtCore.pyqtSignal()
    updatesignal = QtCore.pyqtSignal()
    finishedsignal = QtCore.pyqtSignal()
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        scriptdir=os.path.dirname(os.path.abspath(__file__))
        uifile=os.path.join(scriptdir,'main.ui')
        winicon=os.path.join(scriptdir,'appicon.png')
        
        self.ui = uic.loadUi(uifile)        # load UI
        self.ui.setWindowIcon(QIcon(winicon))
        self.ui.update.clicked.connect(self.onUpdate)        # setup Slots
        self.ui.exit.clicked.connect(self.onAbbrechen)     
        self.ui.fixperm.clicked.connect(lambda: self.fixFilePermissions(WORK_DIRECTORY))
       
        self.onsignal.connect(lambda: self.uienable())    #setup custom slots
        self.offsignal.connect(lambda: self.uidisable())
        self.updatesignal.connect(lambda: self.uiupdate())
        self.finishedsignal.connect(lambda: self.uifinished())
        self.check = True;
        self.line = ""
        
        
        #Switch Button
        layout = self.ui.devLayout
        layout.removeWidget(self.ui.dummySwitch)
        
        
        # Text, LabelOn xPos, Text, LabelOff xPos, width
        switchbtn = SwitchButton(self, "Ja", 15, "Nein", 25, 60)
        layout.addWidget(switchbtn)

        

    def fixFilePermissions(self, folder):
        if folder:
            if folder.startswith('/home/'):  # don't EVER change permissions outside of /home/
                print ("fixing file permissions")
                print(WORK_DIRECTORY)
                chowncommand = "sudo chown -R %s:%s %s" % (USER, USER, folder)
                os.system(chowncommand)
            else:
                print ("exam folder location outside of /home/ is not allowed")
        else:
            print ("no folder given")


    def uienable(self):
        self.ui.update.setEnabled(True)
        line = "Internetanbindung ok!"
        self.ui.inet.setText(line)  
     
     
    def uidisable(self):   
        line = "Keine Internetverbindung!"
        self.ui.inet.setText(line)          
        self.ui.update.setEnabled(False)
        
        
    def uiupdate(self):
        print (self.line)
        self.ui.info.insertPlainText(self.line) 
        self.ui.info.verticalScrollBar().setValue(self.ui.info.verticalScrollBar().maximum())
    
    def onUpdate(self): 
        self.ui.update.setEnabled(False)
        self.check = False;
        update = Updater(self)
        update.start()
    
    def uifinished(self):
        line = "Update Abgeschlossen!"
        self.ui.inet.setText(line)  

    def onAbbrechen(self):    # Exit button
        self.ui.close()
        os._exit(0)
        
    def closeEvent(self, event):
        ''' window tries to close '''
        #stop every running thread set the Flag 
        self.check = False;
        
        

app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
dialog.ui.show()   #show user interface
inet = InetChecker(dialog)
inet.start()   #start inet checking thread

sys.exit(app.exec_())
