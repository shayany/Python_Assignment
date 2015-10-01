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
import datetime

def getContent(url):
    """
    Parameters
    ----------
    url : string("UTF-8")
    
    Returns:
    ________
    Contents of the URL in UTF-8 format.
    """
    if type(url)!=unicode:
        url=url.decode("utf-8")     
    try:    
        return str(urllib.urlopen(url.encode("utf-8")).read()).decode("utf-8")
    except Exception, e:    #Raise exception if the URL is not valid nor unreadable
        print "This URL is not readable!"

def findLink(locationName=""):
    """
    return a list of link(s) to XML file
    
    Parameters
    ----------
    locationName : string (UTF-8)
    
    Returns:
    --------
    If EXISTS(name)=Stadnamn Return all Stadnamn 
    else if EXIST(name)=Kommune Return all Kommune 
    else if EXIST(name)=Kommune Return all Fylke
    else if(name=BLANK STRING) Return all entries 
    else Return EMPTY LIST
    
    """
    if type(locationName)!=unicode:
        locationName=locationName.decode("utf-8")        
    if not(re.match(u"^[A-Za-zåøæÅØÆ\s*?_]*$",locationName)):
        print locationName
        raise  ValueError,"Enter letters/wildcards(* or ?)"
    try:
        plainTextFile=readFromLocalDB(u"http://fil.nrk.no/yr/viktigestader/noreg.txt").lower() #Get content from this URL
        xmlList=[]
        placeName=re.sub(u"[\s]+",u" ",locationName)            #Remove Extra space from the query
        placeName=placeName.lstrip()                             #Remove left spaces
        placeName=placeName.rstrip()                             #Remove right spaces
        placeName=placeName.replace(u"Å",u"å")                   #lower() and upper() does not apply on special characters
        placeName=placeName.replace(u"Ø",u"ø")                   #lower() and upper() does not apply on special characters
        placeName=placeName.replace(u"Æ",u"æ")                   #lower() and upper() does not apply on special characters
        placeName=placeName.replace(u"?",u"[^\\t]?")       #Replace wildcards (this is the format that regex support) 
        placeName=placeName.replace(u"*",u"[^\\t]*?")      #Replace wildcards (this is the format that regex support)
        placeName=placeName.replace(u" ","_")              #There is no space in URL(has been substitued by '_')
        placeName=placeName.lower()                        #Does not apply on special characters 
        plainTextFile=plainTextFile.replace(u"Å",u"å")
        plainTextFile=plainTextFile.replace(u"Ø",u"ø")
        plainTextFile=plainTextFile.replace(u"Æ",u"æ")
        if locationName=="":    
            xmlList = re.findall(u"^.*\\t(.*?)\\r$",plainTextFile,re.IGNORECASE|re.MULTILINE)
            return list(set(xmlList))[1:101] #removing the first line from the file(First line contains titles)
        xmlList = re.findall((u"^.*\\t(http://.*?/place/Norway"
                            "/(?:.*)"    #Fylke
                            "/(?:.*)"    #Kommune
                            "/(?:{0})"   #Stadname
                            "/forecast.xml)\\r$").format(placeName),plainTextFile,re.IGNORECASE|re.MULTILINE)
        if xmlList:
            return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))
        if not xmlList:
            xmlList = re.findall((u"^.*\\t(http://.*?/place/Norway"
                                "/(?:.*)"      #Fylke 
                                "/(?:{0})"     #Kommune
                                "/(?:.*)"      #Stadname   
                                "/forecast.xml)\\r$").format(placeName),plainTextFile,re.IGNORECASE|re.MULTILINE)
            if xmlList:
                return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))
        if not xmlList:        
            xmlList = re.findall((u"^.*\\t(http://.*?/place/Norway"
                                "/(?:{0})"        #Fylke
                                "/(?:.*)"         #Kommune
                                "/(?:.*)"         #Stadname 
                                "/forecast.xml)\\r$").format(placeName),plainTextFile,re.IGNORECASE|re.MULTILINE)    
            if xmlList:
                return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))             
        return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))      
    except Exception:
        print "Empty List (Due to lack of Intenet/No match found)"

def weatherInformation(url):
    """
    return a list that contain all the information about weather and 
    name of the city
    
    Parameters
    ----------
    url : string
    
    Returns:
    --------
    If EXSICT(URL)==TRUE
        [[LOCATION NAME],[(TIME FROM,TIME TO,SYMBOL,PRECIPITATION,WIND SPEED,TEMPERATUR)...()]]
    Else
        Raise Exception
    """
    try:   
        content=getContent(url.lower())
        locationName=re.findall(u"<[^.]*?name[^.]*?>(.*?)<[^.]*?/[^.]*name[^.]*?>",content,re.IGNORECASE+re.MULTILINE)
        weatherContent=re.findall(u"<tabular>(.*?)</tabular>",content,re.IGNORECASE+re.MULTILINE+re.DOTALL)[0]
        timeContent=re.findall((u"<time from=\"(.*?)\" to=\"(.*?)\" period=\"(?:.*?)\">"
                                ".*?<symbol.*?name=\"(.*?)\".*?>.*?"
                                "<precipitation value=\"(.*?)\".*?>.*?"
                                "<windSpeed mps=\"(.*?)\".*?>.*?"
                                "<temperature unit=\"(?:.*?)\" value=\"(.*?)\".*?>")
                                ,weatherContent,re.IGNORECASE+re.MULTILINE+re.DOTALL)
        return [locationName,timeContent]
    except:
        print "Please provide valid URL!"

      
def readfromInternet(query):
    """
    This function get query and based on its pattern redirect it to following methods (Wrapper)
    
    Returns:
    _______
    {query:[timestamp,result]...[,]}
    """
    if re.match(u"^(http://).*?(forecast.xml)$",query,re.IGNORECASE)!=None:       
        return { query : [time.time(),weatherInformation(query)]}
    else:
        return { query : [time.time(),findLink(query)]}
        
def writeToLocalDB(dictionary,fileName):
    """
    Write a dictionary on disk
    
    Parameters:
    ___________
    dictionary:Dictionary that contain your data
    fileName:name of file
    """
    databaseFile=open(fileName,"w") 
    pickle.dump(dictionary,databaseFile)
    databaseFile.close()
                
def readFromLocalDB(query="",expirationTime=21600,testFlag=False):
    """
    Buffering function
    
    Parameteres
    ___________
    query: Can be URL/Name of a location
    expiartionTime: Default 6 hours! After expiration the function get the new file from Internet
    testFlag: If you turn on this flag it will help you to follow the buffering stages (useful for testing)
    Returns
    _______
    temp
    
    If query="Name of a place" Return (list of address for that place)
    Else If query="Address" return a list [[u'Name Of The Place'], [("Time From","Time To", "Symbol", "Precipitation", u"Windspeed", u"Temperature")...()]]
    Else return -1
    """ 
    #The reason I have seperated my buffering is that:
    #    1.It is more flexible due to futue maintenance e.g want to show more result from forecast.xml(next weeks)
    #    2.It has more speed to retrive from 2 files(Instead of 1 big files)
    #    3.has more options for debugging and change the timestamp
    #********************************Start Of Buffering noreg.txt********************************
    
    if re.match(u"^(http://).*?(noreg.txt)$",query,re.IGNORECASE)!=None:
        if os.path.isfile("noreg.txt"):
            norwayPlacesFile=open("noreg.txt","r") 
            norwayPlacesDictionary=pickle.load(norwayPlacesFile)   
            if (time.time()-norwayPlacesDictionary['time']<expirationTime):
                return norwayPlacesDictionary['content']
            else:
                norwayPlacesDictionary['content']=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt")
                norwayPlacesDictionary['time']=time.time()
                norwayPlacesFile.close()
                writeToLocalDB(norwayPlacesDictionary,"noreg.txt")
                return norwayPlacesDictionary['content']                
        else:
            norwayPlacesDictionary={}
            norwayPlacesDictionary['content']=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt")
            norwayPlacesDictionary['time']=time.time()
            writeToLocalDB(norwayPlacesDictionary,"noreg.txt")
            return norwayPlacesDictionary['content']                        
    #********************************End Of Buffering noreg.txt***********************************        
    try:
        query=query.lower()
        databaseFile=open("weatherDB.log","r")  
    except IOError:#File has not found, New file will be created and result written in that file
        weatherDictionary=readfromInternet(query)
        if testFlag==True:#Useful for testing and debuging
            print "File Not Exist,Create File"
        if weatherDictionary[query][1]==[]:#No match find for this query
            return -1
        else:
            writeToLocalDB(weatherDictionary,"weatherDB.log")#result will be written in file
            return weatherDictionary[query][1]             
    else:#If file has been created before, this block will be executed
        weatherDictionary=pickle.load(databaseFile)   
        if(query in weatherDictionary):#Check whether query is in history or not 
            #
            if (time.time()-weatherDictionary[query][0] > expirationTime):   #Default=6Hours 6*60*60 Seconds!(data found in history but it is not valid)
                if testFlag==True:                                           #Useful for testing and debuging
                    print "Data was expired,Reading new data From Internet"
                temp=readfromInternet(query)                                 #New data will retrieve from server
                if temp[query][1]==[]:                                       #No match find for this query
                    return -1
                else:                                                        #result will be written in file
                    weatherDictionary[query]=temp[query]
                    databaseFile.close()
                    writeToLocalDB(weatherDictionary,"weatherDB.log")
                    return weatherDictionary[query][1] 
            if testFlag==True:                                               #Useful for testing and debuging
                print "Data found on history,Reading From a Disk"                    
            return weatherDictionary[query][1]
        else:#Query is not part of the hisotry 
            if testFlag==True:                                               #Useful for testing and debuging
                print "New data has been added to history"
            temp=readfromInternet(query)
            if temp[query][1]==[]:#No match find for this query
                return -1                
            else:#result will be written in file
                weatherDictionary[query]=temp[query]
                databaseFile.close()
                writeToLocalDB(weatherDictionary,"weatherDB.log")
                return weatherDictionary[query][1]
 