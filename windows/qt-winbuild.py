#!/usr/bin/python
# 
# qt-winbuild.py
#

import os
import sys
import xml.dom
import xml.dom.minidom
import datetime
from datetime import datetime
import time
import subprocess
from subprocess import *
import re
import shutil

def getTimeStamp():
    rc = ''
    #Need to use utc for later?
    mynow = datetime.now()
    mytimestampstr = mynow.strftime('%Y_%m_%d_%H_%M_%S')
    rc = mytimestampstr
    return rc
    
class CmdCombiner:
    def __init__(self):
        self.scriptLines = list()
        self.scriptName = ''
        self.logFileName = ''
        self.logging = False
    def addLine(self, string):
        self.scriptLines.append(string + '\n')
    def execute(self, filename, log):
        # Get the script name and log file name from parameters.
        self.scriptName = filename + '.bat'
        self.logFileName = filename + '.log'
        
        # Get the parameter that defines whether the output of the script needs to be logged.
        self.logging = log
        
        # Print the script contents to the temporary script file.
        fh1 = None
        fh1 = open(self.scriptName, 'w', encoding='utf8')
        for line in self.scriptLines:
            fh1.write(line)
        fh1.close()
        
        # Execute the temporary script (and log the output, if the logging parameter has a value of 2.
        fh2 = None
        if self.logging == True:
            fh2 = open(self.logFileName, 'w', encoding='utf8')
        
        outPut = Popen([self.scriptName], stdout=PIPE, stderr=STDOUT, shell=True).communicate()[0]
        output = str(outPut, sys.getdefaultencoding())
        oLines = output.split('\n')
        for oLine in oLines:
            # Print the script output.
            #print ('DEBUG: ' + oLine)
            
            # If logging level is higher than 1, print the script output also to log.
            if self.logging == True:
                fh2.write(oLine)
                fh2.flush()
                
        if self.logging == True:
            fh2.close()
            
class QtWinBuildEnv:
    def __init__(self):
        self.homeDir = 'C:\\USERS\\liaqi\\backup'
        self.sevenZipCommand = 'C:\\APPS\\7zip\\7z.exe'
        self.qtInternalPath = 'D:\\Qt\\qt'
        self.qtPublicPath = 'D:\\Qt\\qt-public'
        self.vcCmd = 'call \"C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\bin\\vcvars32.bat\"'
        self.timeStamp = ''
        self.logFile = ''
        
    def run(self):
        self.timeStamp = getTimeStamp()
        self.logFile = self.homeDir + '\\qt-build-' +  self.timeStamp + '.log'
        self.buildQt('qt', self.qtInternalPath)
        self.buildQt('qt-public', self.qtPublicPath)
        
    def buildQt(self, qtname, qtpath):
        if not os.path.exists(qtpath):
            print ('There is no that path ' + qtpath + '!')
            return
        if not os.path.exists(qtpath + '\\bin'):
            os.makedirs(qtpath + '\\bin')
        buildCmd = CmdCombiner()
        #buildCmd.addLine('@echo off')
        buildCmd.addLine('D:')
        buildCmd.addLine('cd ' + qtpath + '\\bin')
        binBackupFile = self.homeDir + '\\' + qtname + '-bin-backup-' + self.timeStamp + '.zip'
        buildCmd.addLine('\"' + self.sevenZipCommand + '\" a -r -tzip ' + binBackupFile + ' .')
        buildCmd.addLine(self.vcCmd)
        buildCmd.addLine('cd ' + qtpath)
        buildCmd.addLine('set PATH=%PATH%;' + qtpath + '\\bin')
        buildCmd.addLine('call git clean -xfd')
        buildCmd.addLine('call git pull')
        buildCmd.addLine('configure.exe -debug-and-release -confirm-license -opensource')
        buildCmd.addLine('nmake')
        buildCmd.execute(self.homeDir + '\\' + qtname + '-build-' + self.timeStamp, True)
        qtVarsFile = self.homeDir + '\\' + qtname + '-qtvars.bat'
        if os.path.exists(qtVarsFile):
            shutil.copy(qtVarsFile, qtpath + '\\bin\\qtvars.bat')
        
myBuilder = QtWinBuildEnv()
myBuilder.run()
