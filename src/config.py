# -*- coding: utf-8 -*-
import pprint
#parse for php log 
def php_log_parse(logstream):
    while 1:
        l = logstream.readline()
        array = l.split(" ")
        pprint.pprint(array)
        try:
            #第一步先检查是否带时间戳格式;
            if array[0][0]=="[" and array[1][-1]=="]" :
                timestamp = array[0][1:]+" " +array[1][:-1]
                level = array[3]
                msgarray = array[5:]
                print level
                msg = " ".join(msgarray)
                #第5个是error
                if array[2]=="PHP":
                    data = {"type":"CREATE","level":level,"data":msg,"time":timestamp}
                else:
                    data = {"type":"CREATE","level":level,"data":msg,"time":timestamp}
            else:
                data = {"type":"UPDATE","data":l}
        except:
            #只要出错了的,都是追加的消息;
            data = {"type":"UPDATE","data":l}
            pass
        print "data",data
CONFIG={
    "pid":"/tmp/php-log-alert.pid",
    "logfile":"./t.log",
    "callback":php_log_parse
}
