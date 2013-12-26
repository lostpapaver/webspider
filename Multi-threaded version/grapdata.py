#!/usr/bin/env python
#coding=utf8
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import os
import csv
import time
import datetime
import threading
import Queue
class webThreadClass(threading.Thread):
    def __init__(self,que,result_que):
        threading.Thread.__init__(self)
        self.que=que
        self.result_que=result_que
    def get_serverdata(self,url):
        try:
                data = urllib2.urlopen(url).read()
        except:
                data=""
                return "0"
        data_list=[]
        city=re.search(r'id=\'aqiwgttitle2\'> (.*?) Real-time Air Quality Index',data)
        if city:
                data_city=city.group(1)

        else:
                 data_city=""
        time2=re.search(r'Updated on (.*?)</div>',data)
        re_pm25="<td id='cur_pm25' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>([0-9]*?)</td>"
        re_pm10="<td id='cur_pm10' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>([0-9]*?)</td>"
        re_o3="<td id='cur_o3' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>([0-9]*?)</td>"
        re_no2="<td id='cur_no2' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>([0-9]*?)</td>"
        re_so2="<td id='cur_so2' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>([0-9]*?)</td>"
        re_co="<td id='cur_co' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>([0-9]*?)</td>"
        re_temp="<td id='cur_t' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>(.*?)</td>"
        re_dew="<td id='cur_d' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>(.*?)</td>"
        re_pressue="<td id='cur_p' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>(.*?)</td>"
        re_humidity="<td id='cur_h' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>(.*?)</td>"
        re_wind="<td id='cur_w' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>(.*?)</td>"
        pm25=re.search(re_pm25,data)
        pm10=re.search(re_pm10,data)
        o3=re.search(re_o3,data)
        no2=re.search(re_no2,data)
        so2=re.search(re_so2,data)
        co=re.search(re_co,data)
        temp=re.search(re_temp,data)
        dew=re.search(re_dew,data)
        pressue=re.search(re_pressue,data)
        humidity=re.search(re_humidity,data)
        wind=re.search(re_wind,data)

        #
        if time2:
                time_group=time2.group(1)
        else:
                time_group=""
        if pm25:
                pm25_group=pm25.group(1)
        else:
                pm25_group=""
        if pm10:
                pm10_group=pm10.group(1)
        else:
                pm10_group=""
        if o3:
                o3_group=o3.group(1)
        else:
                o3_group=""
        if no2:
                no2_group=no2.group(1)
        else:
                no2_group=""
        if so2:
                so2_group=so2.group(1)
        else:
                so2_group=""
        if co:
                co_group=co.group(1)
        else:
                co_group=""
        if temp:
                temp_group=temp.group(1)
        else:
                temp_group=""
        if dew:
                dew_group=dew.group(1)
        else:
                dew_group=""
        if pressue:
                pressue_group=pressue.group(1)
        else:
                pressue_group=""
        if humidity:
                humidity_group=humidity.group(1)
        else:
                humidity_group=""
        if wind:
                wind_group=wind.group(1)
        else:
                wind_group=""


        data_list.append(data_city)
        data_list.append(time_group)
        data_list.append(pm25_group)
        data_list.append(pm10_group)
        data_list.append(o3_group)
        data_list.append(no2_group)
        data_list.append(so2_group)
        data_list.append(co_group)
        data_list.append(temp_group)
        data_list.append(dew_group)
        data_list.append(pressue_group)
        data_list.append(humidity_group)
        data_list.append(wind_group)
        return data_list

    def run(self):
        while True:
            if not self.que.empty():
                url=self.que.get()
                result=self.get_serverdata(url)

                count=0
                while result=="0":
                    if count>3:
                        break
                    count=count+1
                    result=self.get_serverdata(url)
                
                self.result_que.put(result)
    






def create_data(dir_name):
    filename= dir_name+"\\"+time.strftime("%Y-%m-%d-%H-%M", time.localtime())+".csv"
    writer = csv.writer(file(filename, 'wb'))
    writer.writerow(['city', 'time', 'pm25','pm10','o3','no2','so2','co','temp','temp','dew','pressue','humidity','wind'])
    que=Queue.Queue()
    result_que=Queue.Queue()
    count=0
    urllinks=open("link\\urls\\China.txt","rb")
    link_data=urllinks.readlines()

    urllinks.close()
    i=0
    for url in link_data:
        que.put(url)
    for j in range(20):
        thread_url=webThreadClass(que,result_que)
        thread_url.start()
        
    while True:
        
        flag=0
        print "\r",
        print "%d/%d"%(i,len(link_data)),
        print (i%16)*"*",
        print (i%16)*"\b",
        if not result_que.empty():
            lines=result_que.get()
            i=i+1
            
            for line in lines:
                if line !="":
                    flag=1
            if flag==1:
                if lines!="0":
                    writer.writerow(lines)
                
        else:
            if que.empty():
                break
        


def main():
    start=time.time()
    dir_name=time.strftime("%Y-%m-%d-%H", time.localtime())
    if os.path.isdir(dir_name)==False:
        os.makedirs(dir_name)
        create_data(dir_name)
    end=time.time()
    print "=====the program cost time:",
    print end-start

main()
while 1:

    if time.localtime().tm_min==59:
        time.sleep(60-time.localtime().tm_sec)
        main()
    else:
        time.sleep(60)






