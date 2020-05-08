#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import yaml
from pathlib import Path
from PyQt5 import QtCore, uic, QtWidgets

import time
from PyQt5.Qt import QIcon
from widget.SwitchButton import SwitchButton
import subprocess
from widget.Updater import Updater
from widget.InetChecker import InetChecker

USER = subprocess.check_output("logname", shell=True).rstrip().decode()
USER_HOME_DIR = os.path.join("/home", str(USER))
WORK_DIRECTORY = os.path.join(USER_HOME_DIR, ".life")


class MeinDialog(QtWidgets.QDialog):
    # use signals and slots to talk between the UI dialog and the python thread otherwise it will throw warnings all over the place
    onsignal = QtCore.pyqtSignal()   
    offsignal = QtCore.pyqtSignal()
    updatesignal = QtCore.pyqtSignal(str)
    finishedsignal = QtCore.pyqtSignal()
    
    __config_file = "config.yml" 
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        #rootDir of Application
        self.rootDir = Path(__file__).parent
        uifile=self.rootDir.joinpath('main.ui')
        self.ui = uic.loadUi(uifile)        # load UI
        
        iconfile=self.rootDir.joinpath('appicon.png').as_posix()
        self.ui.setWindowIcon(QIcon(iconfile))  # definiere icon für taskleiste
        
        self.ui.update.clicked.connect(self.onUpdate)        # setup Slots
        self.ui.exit.clicked.connect(self.onAbbrechen)     
        self.ui.fixperm.clicked.connect(lambda: self.fixFilePermissions(WORK_DIRECTORY))
       
        self.onsignal.connect(lambda: self.uienable())    #setup custom slots
        self.offsignal.connect(lambda: self.uidisable())
        self.updatesignal.connect(self.uiupdate)
        self.finishedsignal.connect(lambda: self.uifinished())
        self.check = True;
        
        #Switch Button
        layout = self.ui.devLayout
        layout.removeWidget(self.ui.dummySwitch)        
        
        # Text, LabelOn xPos, Text, LabelOff xPos, width
        self.switchbtn = SwitchButton(self, "Ja", 15, "Nein", 25, 60)
        layout.addWidget(self.switchbtn)
        
        #load Config
        self.loadConfig()
        

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
        
        
    def uiupdate(self, msg):
        self.ui.info.insertPlainText(msg.strip()+"\n") 
        self.ui.info.verticalScrollBar().setValue(self.ui.info.verticalScrollBar().maximum())
        
    
    def onUpdate(self): 
        self.ui.update.setEnabled(False)
        #stop Inet Checker
        self.check = False;
        update = Updater(self, WORK_DIRECTORY)
        update.start()
    
    def uifinished(self):
        line = "Update Abgeschlossen!"
        self.ui.inet.setText(line)  

    def onAbbrechen(self):    # Exit button
        self.check = False;
        self.saveConfig()
        time.sleep(1) 
        self.ui.close()
        os._exit(0)
        
    def log(self, msg):
        ''' send Message to Log Box '''
        print (msg.strip())
        self.updatesignal.emit(msg)
        
    def toggleDev(self):
        if self.switchbtn.getValue():
            line = "life-exam > [Stable] Version!\n"
        else:
            line = "life-exam > [Development] Version!\n"
        self.log(line)
    
    def loadConfig(self):
        if os.path.isfile(self.__config_file): 
            with open(self.__config_file, "r") as ymlfile:
                cfg = yaml.safe_load(ymlfile)
        
            #for section in cfg:
                #print(section)
            #print(cfg["development"])
            #print(cfg["development"]["use"])
            useit = cfg["development"]["use"]
            if useit==0:
                self.switchbtn.setValue(True)
            else:
                self.switchbtn.setValue(False)

            self.branches = {}
            self.branches["stable"] = cfg["development"]["stable_branch"]
            self.branches["dev"] = cfg["development"]["dev_branch"]
        
    def saveConfig(self):
        useit = 1
        if self.switchbtn.getValue():        
            useit = 0 
        data ={
            "development": {
                "stable_branch": "master",
                "dev_branch": "DEV",
                "use": useit,
            },
        }
        
        with open(self.__config_file, "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=False)   
            
        

app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
#show user interface
dialog.ui.show()   

#start inet checking thread
inet = InetChecker(dialog)
inet.start()

sys.exit(app.exec_())