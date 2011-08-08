# -*- coding: utf-8 -*-
#================================================
import sys
#sys.path.append("/var/lib/python-support/python2.5/")
#sys.path.append("/var/lib/python-support/python2.6/")
#sys.path.append("/usr/share/pyshared/")
#sys.path.append("/usr/lib/pymodules/python2.6/")
import sys
import os
import atexit
import getopt
import json
import threading
import signal, os,time,re
import imp
import shutil

import pcolor
import pprint
"""
"""

__author__ = "xurenlu"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 xurenlu"
__license__ = "LGPL"

def sig_exit():
    """ handle the exit signal
    """
    print "[end time]:"+str(time.time())
    print pcolor.pcolorstr("CAUGHT SIG_EXIT signal,exiting...",pcolor.PHIGHLIGHT,pcolor.PRED,pcolor.PBLACK)
    global config
    os.remove(config["pid"])
    sys.exit()

def handler(signum, frame):
    """
    handle signals
    """
    sig_exit()
    if signum == 3:
        sig_exit()
    if signum == 2:
        sig_exit()
    if signum == 9:
        sig_exit()
        return None

def prepare_taskfile(taskfile):
    """Attempt to load the taskfile as a module.
    """
    path = os.path.dirname(taskfile)
    taskmodulename = os.path.splitext(os.path.basename(taskfile))[0]
    fp, pathname, description = imp.find_module(taskmodulename, [path])
    #print "fp:",fp,",pathname:",pathname,",desc:",description
    try:
        return imp.load_module(taskmodulename, fp, pathname, description)
    finally:
        if fp:
            fp.close()

def inittask(task,type="web"):
    """init a task and create empty files for you 
    """
    try:
        os.mkdir(task,0755)
    except Exception,e:
        print "exception:",e
        pass
    try:
        shutil.copyfile("share/templates/project-%s.py" % type,"%s/%s.py" % (task,task) )
    except Exception,e:
        print "exception:",e
        pass
    try:
        shutil.copyfile("share/templates/config-%s.py" % type,"%s/config.py" % task )
    except:
        pass

def handle_pid(pidfile):
    """
    handle pid files
    """
    pid=os.getpid()
    try:
        lastpid=int(open(pidfile).read())
    except:
        lastpid=0
        pass
    try:
        if lastpid>0:
            os.kill(lastpid,3)
    except:
        pass
    fp=open(pidfile,"w")
    fp.write(str(pid))
    fp.close()

def at_exit():
    """
    hook of exit
    """
    end_time=time.time()
    print "[end time]:"+str(end_time)
    print "[cost time]:"+str(end_time-start_time)
    print "\n=========================\n"

def usage():
    print "usage:\t",sys.argv[0],' init task' 
    print "usage:\t",sys.argv[0],' run taskfile' 
    print "usage:\t",sys.argv[0],' help' 


def handle_log(logfile,callback):
    pw,pr = os.popen2("tail -f %s" % logfile,"rw");
    callback(pr) 

def stop_process(pidfile):
    try:
        lastpid=int(open(pidfile).read())
    except:
        lastpid=0
        pass
    try:
        if lastpid>0:
            os.kill(lastpid,3)
    except:
        print "exit failed."
    

signal.signal(signal.SIGINT,handler)
signal.signal(signal.SIGTERM,handler)
signal.signal(3,handler)

#如果子进程退出时主进程不需要处理资源回收等问题
#这样可以避免僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
start_time=time.time()

if len(sys.argv)<2:
    usage()
    sys.exit()

cmd=sys.argv[1].lower()
if cmd == "help" :
    usage()
    sys.exit()

elif cmd == "start":
    '''run a single file'''
    print "[start time]:"+str(start_time)
    atexit.register(at_exit)
    taskfile=sys.argv[-1]
    k=prepare_taskfile(taskfile)
    global config
    config = k.CONFIG
    handle_pid(k.CONFIG["pid"])
    handle_log(k.CONFIG["logfile"],k.CONFIG["callback"])

elif cmd == "stop":
    '''run a single file'''
    print "[start time]:"+str(start_time)
    atexit.register(at_exit)
    taskfile=sys.argv[-1]
    k=prepare_taskfile(taskfile)
    global config
    config = k.CONFIG
    stop_process(config["pid"])

elif cmd == "init":
    task=sys.argv[2]
    if len(sys.argv)>3:
        task=sys.argv[3]
    else:
        task="web"
    type="vertical"
    inittask(task,type)

else:
    usage()
    sys.exit()
