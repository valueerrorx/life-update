#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import threading
import time
import socket

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