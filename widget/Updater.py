#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import threading
import time

class Updater(threading.Thread):
    """ 
    in order to provide a NONBLocking loop that 
    periodically checks the internet connection 
    this is done it a separate thread
    """
    def __init__(self, mainui, work_directory):
        threading.Thread.__init__(self)
        self.mainui= mainui
        self.stop = False
        self.work_directory = work_directory

    def run(self):
        while self.stop == False:
            self.update()
            time.sleep(5)
            
            
    def update(self):
        #update life EXAM
        branches = self.mainui.branches 
        self.log("Updating LiFE Exam...\n")
        
        #do we use DEV Version of life-exam, or stable
        #stable ... main, Development ... DEV
        cmd = "cd %s/applications/life-exam " %(self.work_directory)
        print(cmd)
        
        #switch to branch https://bluecast.tech/blog/git-switch-branch/
git switch SMan-Test
        
    def work(self):
        #&& git pull
        
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
        
        cmd = "cd %s/applications/life-nextcloudusers && git pull " %(self.work_directory)
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
        
        cmd = "cd %s/applications/life-update && git pull " %(self.work_directory)
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
        
        cmd = "cd %s/applications/life-firststart && git pull " %(self.work_directory)
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
        
        cmd = "cd %s/applications/life-builder && git pull " %(self.work_directory)
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
        
        cmd = "cd %s/applications/life-kiosk && git pull " %(self.work_directory)
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