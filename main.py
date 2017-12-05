#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtGui import *

import subprocess



USER = subprocess.check_output("logname", shell=True).rstrip()
USER_HOME_DIR = os.path.join("/home", str(USER))



class MeinDialog(QtWidgets.QDialog):

        
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        scriptdir=os.path.dirname(os.path.abspath(__file__))
        uifile=os.path.join(scriptdir,'main.ui')
        winicon=os.path.join(scriptdir,'appicon.png')
        
        self.ui = uic.loadUi(uifile)        # load UI
        self.ui.setWindowIcon(QIcon(winicon))
        self.ui.update.clicked.connect(self.onUpdate)        # setup Slots
        self.ui.exit.clicked.connect(self.onAbbrechen)     
       
   




        
    
    
    def onUpdate(self):  
    
        cmd = "cd ~/.life/applications/life-exam && git pull " 

        proc = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stderr.readline, b''):
            print line, self.ui.info.insertPlainText(line)
        for line in iter(proc.stdout.readline, b''):
            print line, self.ui.info.insertPlainText(line)  
        proc.communicate()     
        
        cmd = "cd ~/.life/applications/life-usbcreator && git pull " 

        proc = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stderr.readline, b''):
            print line, self.ui.info.insertPlainText(line)
        for line in iter(proc.stdout.readline, b''):
            print line, self.ui.info.insertPlainText(line)  
        proc.communicate()     
    
        
       


    def onAbbrechen(self):    # Exit button
        self.ui.close()
        os._exit(0)










app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
dialog.ui.show()   #show user interface
sys.exit(app.exec_())
