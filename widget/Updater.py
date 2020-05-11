#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import threading
import time
import os

class Updater(threading.Thread):
    """ 
    in order to provide a NONBLocking loop that 
    periodically checks the internet connection 
    this is done it a separate thread
    """
    def __init__(self, mainui, work_directory, user):
        threading.Thread.__init__(self)
        self.mainui= mainui
        self.stop = False
        self.work_directory = work_directory
        self.user = user

    def run(self):
        while self.stop == False:
            self.update()
            time.sleep(5)
            
    def runCmd(self, cmd):
        ''' runs a command '''
        proc = subprocess.Popen(cmd,  shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
        for line in iter(proc.stderr.readline, b''):
            self.mainui.log(line.decode())
        
        for line in iter(proc.stdout.readline, b''):
            self.mainui.log(line.decode())
            
            
        proc.communicate()
        time.sleep(0.5)
        
    def fixFilePermissions(self, folder):
        if folder:
            # don't EVER change permissions outside of /home/
            if folder.startswith('/home/'):  
                print ("fixing file permissions %s" % folder)
                #cmd = ['sudo', 'chown', '-R', '%s:%s' % (self.user, self.user), folder]
                #self.runCmd(cmd)
                
                command = "sudo chown -R %s:%s %s" % (self.user, self.user, folder)
                print(command)
                os.system(command)
            else:
                print ("exam folder location outside of /home/ is not allowed")
        else:
            print ("no folder given")
            
    def update(self):
        #first check permissions
        self.fixFilePermissions(self.work_directory)
        #update life EXAM ----------------------------------------------------------------------------------
        branches = self.mainui.branches
        if self.mainui.switchbtn.getValue():
            active_branch = branches["dev"]
        else:
            active_branch = branches["stable"]
            
        self.mainui.log("Updating LiFE Exam...\n")
        #switch to branch https://bluecast.tech/blog/git-switch-branch/
        
        #do we use DEV Version of life-exam, or stable
        #stable ... main, Development ... DEV
        
        #step1 back to https
        cmd = "cd %s/applications/life-exam " % (self.work_directory)
        cmd += "&& git remote set-url origin https://github.com/valueerrorx/life-exam.git"
        self.runCmd(cmd)
        
        #step 2
        cmd = "cd %s/applications/life-exam " % (self.work_directory)
        cmd += "&& git checkout %s" % (active_branch)
        self.runCmd(cmd)
        
        #step 3
        cmd = "cd %s/applications/life-exam " % (self.work_directory)
        cmd += "&& git pull"
        self.runCmd(cmd)


        #update life nextcloudusers ----------------------------------------------------------------------------------
        self.mainui.log("\nUpdating LiFE Nextcloudusers...\n")
        cmd = "cd %s/applications/life-nextcloudusers && git pull " %(self.work_directory)
        self.runCmd(cmd)
        
        
        #update life UPDATE ----------------------------------------------------------------------------------
        self.mainui.log("\nUpdating LiFE Update...\n")
        #step1 back to https
        cmd = "cd %s/applications/life-update " % (self.work_directory)
        cmd += "&& git remote set-url origin https://github.com/valueerrorx/life-update.git"
        self.runCmd(cmd)
        
        cmd = "cd %s/applications/life-update && git pull " %(self.work_directory)
        self.runCmd(cmd)
     
     
        #update life FIRSTSTART ----------------------------------------------------------------------------------
        self.mainui.log("\nUpdating LiFE Firststart...\n")        
        cmd = "cd %s/applications/life-firststart && git pull " %(self.work_directory)
        self.runCmd(cmd)
     
        
        #update life builder ----------------------------------------------------------------------------------
        self.mainui.log("\nUpdating LiFE Builder...\n")                
        cmd = "cd %s/applications/life-builder && git pull " %(self.work_directory)
        self.runCmd(cmd) 
        
        
        #update life kiosk ----------------------------------------------------------------------------------
        self.mainui.log("\nUpdating LiFE Kiosk...\n")
        
        cmd = "cd %s/applications/life-kiosk && git pull " %(self.work_directory)
        self.runCmd(cmd)


        self.mainui.finishedsignal.emit()
        self.stop = True
