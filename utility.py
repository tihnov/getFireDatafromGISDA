import socket 
import datetime
import subprocess
import time
import os
import sys
import base64
import binascii
import logging 
import logging.handlers
import io
import re
import unicodedata
from logging.handlers import TimedRotatingFileHandler
from getmac import getmac
# from kalman import kalman as km
import json
import requests
import hashlib


FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")

class log() :

    strip_unicode = re.compile(r"([^-_a-zA-Z0-9!@#%&=,/'\"\'\\;:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\]+|[^\s]+)")
    logg = logging.getLogger()
    prevtimeStamp = datetime.datetime.utcnow()
    currentTime = datetime.datetime.utcnow()
    diffTime = None
    req_count = 0
    # dirpath = os.path.dirname(sys.argv[0])
    dir_path = os.path.abspath(os.path.dirname(sys.argv[0])).replace("/bin", "")

    logFileName = "log"
    logFileCount = 30
    logFilePeriod = datetime.timedelta(days = 30)
    logPath = ""
    level = {
        "DEBUG" : 0,
        "INFO" : 1,
        "WARNING" : 2,
        "ERROR" : 3,
        "CRITICAL" : 4
    }

    def clean(self):
        thisTime = datetime.datetime.now()
        startTime = thisTime-self.logFilePeriod
        arr = os.listdir("{}/log".format(self.dir_path))
        # self.log("this DIR : {}".format(self.dir_path), "INFO")
        # self.log("list file : {}".format(arr), "INFO")
        # self.log("thisTime : {}".format(thisTime), "INFO")
        # self.log("startTime : {}".format(startTime), "INFO")
        while len(arr) > 0:
            f = arr.pop()
            # self.log("thisName : {}".format(f), "INFO")
            # fdate = f[:15]
            fdate = f.split("_")[0]
            # self.log("fdate : {}".format(fdate), "INFO")
            dfdate = datetime.datetime.strptime(fdate,"%Y%m%d")
            # self.log("dfdate : {}".format(dfdate), "INFO")
            if (self.logFileName in f) and (dfdate < startTime) :
                thisfile = "{}/log/{}".format(self.dir_path, f)
                self.log("delete thisName : {}".format(thisfile), "INFO")
                if os.path.exists(thisfile):
                    os.remove(thisfile)
                else:
                    self.log("{} does not exist".format(thisfile), "INFO")


    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler
    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.logPath, 
                                                when='D', 
                                                backupCount = self.logFileCount,
                                                encoding="utf-8",
                                                utc=True)
        file_handler.setFormatter(FORMATTER)
        return file_handler
    
    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG) # better to have too much log than not enough
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger

    def __init__(self,thisFile = None, thisCount = None, period = None):
        self.versions = "1.0a"
        if thisFile:
            self.logFileName = thisFile
        if thisCount:
            self.logFileCount = thisCount
        if period :
            self.logFilePeriod = datetime.timedelta(days = period)

        self.currentTime = datetime.datetime.utcnow()
        # self.logFileName = thisFile
        logFile = 'log/{}_{}'.format(self.currentTime.strftime("%Y%m%d_%H%M%S"),self.logFileName)
        self.logPath = '{}/{}'.format(self.dir_path,logFile)
        # self.logg.setLevel(logging.DEBUG)
        # print("logPath : {} - logFile : {}".format(self.logPath, logFile))
        self.logg = self.get_logger(self.logPath)
        # handler = logging.FileHandler(self.logPath,mode='a')
        # rotatehandler = logging.handlers.RotatingFileHandler(self.logPath, 
        #                                             mode='a',
        #                                             maxBytes=10000,
        #                                             backupCount = 5)
        # self.logg.addHandler(handler)
        # self.logg.addHandler(rotatehandler)
        # self.logg.setLevel(logging.DEBUG)
        self.timeStampFormat()
        s ='Start warning Logging to : {}'.format(self.logPath)
        self.logg.warning(s.encode("utf-8"))
        s ='Start info Logging to : {}'.format(self.logPath)
        self.logg.info(s.encode("utf-8"))
        s ='Start debug Logging to : {}'.format(self.logPath)
        self.logg.debug(s.encode("utf-8"))        

    def timeStampFormat(self):
        self.currentTime = datetime.datetime.utcnow()
        self.diffTime = self.currentTime - self.prevtimeStamp

    def log(self,s = None , logtype = None):
        t = logtype.upper()
        self.timeStampFormat()
        # print("1 {}".format(s.encode("utf-8")))
        s = self.strip_unicode.sub('', s)
        # print("2 {}".format(s.encode("utf-8")))
        s ='[{}] | {}'.format(self.diffTime ,s.strip())   
        # print("3 {}".format(s.encode("utf-8")))     
        if t in self.level:
            l = self.level.get(t)
            if l == 0:
                self.logg.debug(s.encode("utf-8")) 
            elif l == 1:
                self.logg.info(s.encode("utf-8")) 
            elif l == 2:
                self.logg.warning(s.encode("utf-8")) 
            elif l == 3:
                self.logg.error(s.encode("utf-8")) 
            elif l == 4:
                self.logg.critical(s.encode("utf-8"))                 
            else:
                self.logg.info(s.encode("utf-8"))    
        else:
            self.logg.info(s.encode("utf-8"))  

class ServiceMonitor(object):

    def __init__(self, service):
        self.service = service

    def is_active(self):
        bool_status = False
        list_status = list()
        time.sleep(5)
        """Return True if service is running"""
        cmd = '/bin/systemctl status {}.service'.format(self.service)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,encoding='utf8')
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0].split('\n')
        # print("stdout_list status : {}".format(stdout_list))
        for line in stdout_list:
            # print("line : {}".format(line.strip()))
            list_status.append(line.strip())
            if 'Active:' in line:
                if '(running)' in line:
                    bool_status = True
        return bool_status , list_status

    def start(self):
        bool_status = False
        list_status = list()
        list_status.append("start : {}".format(self.service))
        cmd = '/bin/systemctl start {}.service'.format(self.service)
        list_status.append("$$$ : {}".format(cmd))
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0]
        # print("start : {}".format(self.service)) 
        time.sleep(5)
        cmd = '/bin/systemctl status {}.service'.format(self.service)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,encoding='utf8')
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0].split('\n')
        # print("start {} - status : {}".format(self.service, stdout_list))
        for line in stdout_list:
            # print("line : {}".format(line.strip()))
            list_status.append(line.strip())
            if 'Active:' in line:
                if '(running)' in line:
                    bool_status = True
        return bool_status , list_status  

    def restart(self):
        bool_status = False
        list_status = list()
        list_status.append("restart : {}".format(self.service))
        cmd = '/bin/systemctl restart {}.service'.format(self.service)
        list_status.append("$$$ : {}".format(cmd))
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0]
        # print("restart : {}".format(self.service))
        time.sleep(5)
        cmd = '/bin/systemctl status {}.service'.format(self.service)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,encoding='utf8')
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0].split('\n')
        # print("restart {} status : {}".format(self.service, stdout_list))
        for line in stdout_list:
            # print("line : {}".format(line.strip()))
            list_status.append(line.strip())
            if 'Active:' in line:
                if '(running)' in line:
                    bool_status = True
        return bool_status , list_status  

    def stop(self):
        bool_status = False
        list_status = list()
        list_status.append("stop : {}".format(self.service))
        cmd = '/bin/systemctl stop {}.service'.format(self.service)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0]
        # print("stop : {}".format(self.service))
        time.sleep(5)
        cmd = '/bin/systemctl status {}.service'.format(self.service)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,encoding='utf8')
        # print("proc : {}".format(proc))
        stdout_list = proc.communicate()[0].split('\n')
        # print("stop {} status : {}".format(self.service, stdout_list))
        for line in stdout_list:
            # print("line : {}".format(line.strip()))
            list_status.append(line.strip())
            if 'Active:' in line:
                if '(running)' in line:
                    bool_status = True
        return bool_status , list_status 

class HWinfo(object):
    versions = "1.0a"
    def __init__(self):
        self.versions = "1.0a"
    
    def thisMAC(self):
        return str(getmac.get_mac_address()).replace(':','').strip().upper()

    def thatMAC(self,targetIP = None):
        if targetIP:
            return str(getmac.get_mac_address(ip=targetIP, network_request=True)).replace(':','').upper()
        return None

    def thisDiskSerial(self):
        lsblk = subprocess.run(['lsblk','-J','-o','NAME,SERIAL,MOUNTPOINT'],stdout=subprocess.PIPE,encoding='utf8')
        for dev in json.loads(lsblk.stdout)['blockdevices']:
            if dev['name'] == 'mmcblk0':
                return str(dev['serial']).replace("0x",'').strip().upper()
        return None
    
# class licManagement(object):
#     versions = "1.0a"
#     thisMAC = ""
#     thisDiskSerial = ""
#     thisHW = HWinfo()
#     dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))
#     kmc = "abcdefgh"
#     kalman = km(kmc)
#     thisURL = ""

#     def __init__(self):
#         self.versions = "1.0a"
#         self.thisMAC = self.thisHW.thisMAC()
#         self.thisDiskSerial = self.thisHW.thisDiskSerial()
#         arr = os.listdir("{}".format(self.dir_path))
    
#     # Request new License
#     def licRequest(self):
#         ret = requests.post(self.thisURL, json=requestData, headers=headers)
#     # True is valid, False is in