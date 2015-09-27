# -*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8
from subprocess import Popen,PIPE
import re
import urllib
import cPickle as pickle
import sys
import os 
import time
"""
def readFromLocalDB(locationName):
    try:
        databaseFile=open("weather.log","r")  
    except IOError:#File has not found, New file will be created and result written in that file
        weatherDictionary={}
        weatherDictionary=readfromInternet(locationName,weatherDictionary)
        if not weatherDictionary:
            print "Nothing"
        else:
            #databaseFile.close()
            writeToLocalDB(weatherDictionary)
            return weatherDictionary[locationName.encode("utf-8")][1]             
    else:
        weatherDictionary=pickle.load(databaseFile)
        print weatherDictionary
        if(locationName.encode("utf-8") in weatherDictionary):
            if time.time()-weatherDictionary[locationName.encode("utf-8")][0]>60:                                            
                print "This is not valid result"
                weatherDictionary=readfromInternet(locationName,weatherDictionary)
                if not weatherDictionary:
                    print "Nothing"                    
                else:
                    databaseFile.close()
                    writeToLocalDB(weatherDictionary)
                    return weatherDictionary[locationName.encode("utf-8")][1]                            
            else:#VALID
                databaseFile.close()                
                return weatherDictionary[locationName.encode("utf-8")][1]
        else:
            weatherDictionary=readfromInternet(locationName,weatherDictionary)
            if not weatherDictionary:
                print "Nothing"                    
            else:
                databaseFile.close()
                writeToLocalDB(weatherDictionary)
                return weatherDictionary[locationName.encode("utf-8")][1]                                                 
"""
def getContent(url):
    """
    Return contents of the URL.
    """
    return str(urllib.urlopen(url.encode("utf-8")).read()).decode("utf-8")
    #stringmy =Popen("curl http://fil.nrk.no/yr/viktigestader/noreg.txt",stdout=PIPE).communicate()[0]
    #print stringmy



def findLink(name=""):
    """
    return link to XML file based on the name
    
    Parameters
    ----------
    name : string
    
    Returns:
    --------
    If EXISTS(name)=TRUE Return all Stadnamn | Kommune | Fylke.
    else if(name=BLANK STRING) Return all entries 
    else Return EMPTY LIST
    
    """
    if not(re.match(u"^[A-Za-zåøæÅØÆ\s*?]*$",name)):
       raise  ValueError,"Enter only letters or wildcards(* or ?)"
    plainTextFile=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt") #Get content from this URL
    xmlList=[]#Create Empty list to return results 
    cityName=name.upper()
    cityName=cityName.replace("?","[^\\t]?")    #Replace wildcards (this is the format that regex support) 
    cityName=cityName.replace("*","[^\\t]*?")    #Replace wildcards (this is the format that regex support) 
    if name=="":    
        xmlList = re.findall(u"^.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
        return list(set(xmlList))[1:] #removing the first line from the file(Titles)
    xmlList = re.findall(u"^\\d*\\t{0}\\t.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
    if xmlList:
        return list(set(xmlList))   
    
    if not xmlList:
        xmlList = re.findall(u"^\\d*\\t.*?\\t.*?\\t.*?\\t.*?\\t.*?\\t{0}\\t.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
        if xmlList:
            list(set(xmlList))    
    if not xmlList:
        xmlList = re.findall(u"^\\d*\\t(?:.*?\\t){6}%s\\t.*\\t(.*?)\\r$"%cityName,plainTextFile,re.I+re.MULTILINE)
        #xmlList = re.findall(u"^\\d*\\t.*?\\t.*?\\t.*?\\t.*?\\t.*?\\t.*?\\t{0}\\t.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
        if xmlList:
            list(set(xmlList))       
    return list(set(xmlList))


def weatherInformation(url):    
    content=getContent(url)
    locationName=re.findall(u"<[^.]*?name[^.]*?>(.*?)<[^.]*?/[^.]*name[^.]*?>",content,re.I+re.MULTILINE)
    weatherContent=re.findall(u"<tabular>(.*?)</tabular>",content,re.I+re.MULTILINE+re.DOTALL)[0]
    timeContent=re.findall((u"<time from=\"(.*?)\" to=\"(.*?)\" period=\"(?:.*?)\">"
                            ".*?<symbol.*?name=\"(.*?)\".*?>.*?"
                            "<precipitation value=\"(.*?)\".*?>.*?"
                            "<windSpeed mps=\"(.*?)\".*?>.*?"
                            "<temperature unit=\"(?:.*?)\" value=\"(.*?)\".*?>")
                            ,weatherContent,re.I+re.MULTILINE+re.DOTALL)
    return [locationName,timeContent]
    
    
def readfromInternet(query):    
    if re.match(u"^http://.*",query)==None:
        return { query : [time.time(),findLink(query)]}
    else:
        return { query : [time.time(),weatherInformation(query)]}
        
        
        
def writeToLocalDB(weatherDictionary):
    databaseFile=open("weather.log","w") 
    pickle.dump(weatherDictionary,databaseFile)
    databaseFile.close()
        
        
def pp():
    databaseFile=open("weather.log","r")
    weatherDictionary=pickle.load(databaseFile)
    print weatherDictionary  
        
def readFromLocalDB(query):
    try:
        query=query.upper()
        databaseFile=open("weather.log","r")  
    except IOError:#File has not found, New file will be created and result written in that file
        weatherDictionary=readfromInternet(query)
        if not weatherDictionary:
            return -1
            print "Nothing"
        else:
            writeToLocalDB(weatherDictionary)
            return weatherDictionary[query][1]             
    else:#If file has been created before, this block will be executed
        weatherDictionary=pickle.load(databaseFile)
        if(query in weatherDictionary):
            """
            This part has been added for timing 
            """
            if (time.time()-weatherDictionary[query][0] > 60):  ############TIMING##########
                temp=readfromInternet(query)
                if not temp:
                    return -1
                    print "Nothing"
                else:
                    weatherDictionary[query]=temp[query]
                    databaseFile.close()
                    writeToLocalDB(weatherDictionary)
                    return weatherDictionary[query][1] 
            """
            This part has been added for timing
            """
            return weatherDictionary[query][1]
        else:
            temp=readfromInternet(query)
            if not temp:
                return -1                
                print "Nothing"
            else:
                weatherDictionary[query]=temp[query]
                databaseFile.close()
                writeToLocalDB(weatherDictionary)
                return weatherDictionary[query][1]                                 




