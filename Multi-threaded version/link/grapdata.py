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



def get_serverdata(url):
    try:
        data = urllib2.urlopen(url).read()
    except:
        data=""
        return "0"

    p=re.compile(r'<h1>(.{1,15}?)</h1>')
    country_list=p.split(data)
    #print country_list
    country_names=p.findall(data)
        
    
    return (country_list,country_names)
          
        


def get_urllink(data_link):
    p=re.compile(r"href='(http.*?)'>")
    links=p.findall(data_link)
    return links




def main():
    
   
    
    url="http://aqicn.org/city/all/"
    if get_serverdata(url)!="0":
        country_list,country_names=get_serverdata(url)
        for li in country_list:
            if li.find("href")<0:
                #print "1"
                country_list.remove(li)
    for i in range(0,len(country_list)):
        if i>1 and i<len(country_names) :
            #print country_list[i]
            
            filename=country_names[i-1]+".txt"
            temp=open(filename,"wb+")
            links=get_urllink(country_list[i])
            for link in links:
                temp.write(link+"\n")
            temp.close()
            
            
            
        
    
    
        
main()
    




