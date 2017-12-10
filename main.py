#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtGui import *

import subprocess
import threading
import time
import socket

USER = subprocess.check_output("logname", shell=True).rstrip()
USER_HOME_DIR = os.path.join("/home", str(USER))



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
    
        cmd = "cd ~/.life/applications/life-exam && git pull " 
        proc = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stderr.readline, b''):
            self.mainui.line = line
            self.mainui.updatesignal.emit()
        for line in iter(proc.stdout.readline, b''):
            self.mainui.line = line
            self.mainui.updatesignal.emit()
        proc.communicate()     
        
        
        
        #update life USBCREATOR
        line = "\nUpdating LiFE USBCreator...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd ~/.life/applications/life-usbcreator && git pull " 
        proc = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stderr.readline, b''):
            self.mainui.line = line
            self.mainui.updatesignal.emit()
        for line in iter(proc.stdout.readline, b''):
            self.mainui.line = line
            self.mainui.updatesignal.emit()
        proc.communicate()
        
        
        
        #update life UPDATE
        line = "\nUpdating LiFE Update...\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
        
        cmd = "cd ~/.life/applications/life-update && git pull " 
        proc = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stderr.readline, b''):
            self.mainui.line = line
            self.mainui.updatesignal.emit()
        for line in iter(proc.stdout.readline, b''):
            self.mainui.line = line
            self.mainui.updatesignal.emit()
        proc.communicate() 
        
        self.stop = True
        line = "\nFinished!\n"
        self.mainui.line = line
        self.mainui.updatesignal.emit()
            
  






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
            print "online"
            self.mainui.onsignal.emit()
            return True
        except:
            print "offline"        
            self.mainui.offsignal.emit()
            return False





class MeinDialog(QtWidgets.QDialog):
    onsignal = QtCore.pyqtSignal()   # use signals and slots to talk between the UI dialog and the python thread otherwise it will throw warnings all over the place
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
       
        self.onsignal.connect(lambda: self.uienable())    #setup custom slots
        self.offsignal.connect(lambda: self.uidisable())
        self.updatesignal.connect(lambda: self.uiupdate())
        self.finishedsignal.connect(lambda: self.uifinished())
        self.check = True;
        self.line = ""

    def uienable(self):
        self.ui.update.setEnabled(True)
        line = "Internetverbindung aktiv!"
        self.ui.inet.setText(line)  
     
     
    def uidisable(self):   
        line = "Keine Internetverbindung!"
        self.ui.inet.setText(line)  
        
        self.ui.update.setEnabled(False)
        
        
    def uiupdate(self):
        self.ui.info.insertPlainText(self.line)  
    
    def onUpdate(self): 
        self.check = False;
        update = Updater(self)
        update.start()
    
    def uifinished(self):
        line = "Update Abgeschlossen!"
        self.ui.inet.setText(line)  
       


    def onAbbrechen(self):    # Exit button
        self.ui.close()
        os._exit(0)










app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
dialog.ui.show()   #show user interface
inet = InetChecker(dialog)
inet.start()   #start inet checking thread

sys.exit(app.exec_())
