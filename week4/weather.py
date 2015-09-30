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
    return str(urllib.urlopen(url.encode("utf-8")).read()).decode("utf-8")


def findLink(locationName=""):
    """
    return a list of link(s) to XML file
    
    Parameters
    ----------
    name : string
    
    Returns:
    --------
    If EXISTS(name)=Stadnamn Return all Stadnamn 
    else if EXIST(name)=Kommune Return all Kommune 
    else if EXIST(name)=Kommune Return all Fylke
    else if(name=BLANK STRING) Return all entries 
    else Return EMPTY LIST
    
    """
    if not(re.match(u"^[A-Za-zåøæÅØÆ\s*?_]*$",locationName)):
       raise  ValueError,"Enter only letters or wildcards(* or ?)"
    plainTextFile=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt").lower() #Get content from this URL
    xmlList=[]
    cityName=re.sub(u"[\s]+",u" ",locationName)            #Remove Extra space from the query
    cityName=cityName.replace(u"Å",u"å")
    cityName=cityName.replace(u"Ø",u"ø")
    cityName=cityName.replace(u"Æ",u"æ")
    cityName=cityName.replace(u"?",u"[^\\t]?")       #Replace wildcards (this is the format that regex support) 
    cityName=cityName.replace(u"*",u"[^\\t]*?")      #Replace wildcards (this is the format that regex support)
    cityName=cityName.replace(u" ","_")              #There is no space in URL(has been substitued by '_')
    cityName=cityName.lower()                        #Does not apply on special characters 
    plainTextFile=plainTextFile.replace(u"Å",u"å")
    plainTextFile=plainTextFile.replace(u"Ø",u"ø")
    plainTextFile=plainTextFile.replace(u"Æ",u"æ")
    if locationName=="":    
        xmlList = re.findall(u"^.*\\t(.*?)\\r$",plainTextFile,re.IGNORECASE|re.MULTILINE)
        return list(set(xmlList))[1:101] #removing the first line from the file(Titles)
    xmlList = re.findall((u"^.*\\t(http://.*?/place/Norway"
                          "/(?:.*)"    #Fylke
                          "/(?:.*)"    #Kommune
                          "/(?:{0})"   #Stadname
                          "/forecast.xml)\\r$").format(cityName),plainTextFile,re.IGNORECASE|re.MULTILINE)
    if xmlList:
        return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))
    if not xmlList:
        xmlList = re.findall((u"^.*\\t(http://.*?/place/Norway"
                              "/(?:.*)"      #Fylke 
                              "/(?:{0})"     #Kommune
                              "/(?:.*)"      #Stadname   
                              "/forecast.xml)\\r$").format(cityName),plainTextFile,re.IGNORECASE|re.MULTILINE)
        if xmlList:
            return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))
    if not xmlList:        
        xmlList = re.findall((u"^.*\\t(http://.*?/place/Norway"
                              "/(?:{0})"        #Fylke
                              "/(?:.*)"         #Kommune
                              "/(?:.*)"         #Stadname 
                              "/forecast.xml)\\r$").format(cityName),plainTextFile,re.IGNORECASE|re.MULTILINE)    
        if xmlList:
            return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))             
    return list(set(xmlList))[0:100] if len(list(set(xmlList))[0:100]) else list(set(xmlList))      


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
    
def readfromInternet(query):
    if re.match(u"^http://.*",query,re.IGNORECASE)==None:        
        return { query : [time.time(),findLink(query)]}
    else:
        return { query : [time.time(),weatherInformation(query)]}
    
                    
def writeToLocalDB(weatherDictionary):
    """
    Write a dictionary on disk
    
    Parameters:
    ___________
    weatherDictionary
    """
    databaseFile=open("weatherDB.log","w") 
    pickle.dump(weatherDictionary,databaseFile)
    databaseFile.close()
        
        
def readFromLocalDB(query="",expirationTime=10,testFlag=False):
    """
    Buffering function
    
    Parameteres
    ___________
    query: Can be URL/Name of a location
    expiartionTime: Default 6 hours! After expiration the function get the new file from Internet
    Returns
    _______
    If query="Name of a place" Return list of address for that place
    Else If query="Address" return a list [[u'Name Of The Place'], [("Time From","Time To", "Symbol", "Precipitation", u"Windspeed", u"Temperature")...()]]
    Else return -1
    """
    try:
        query=query.lower()
        databaseFile=open("weatherDB.log","r")  
    except IOError:#File has not found, New file will be created and result written in that file
        weatherDictionary=readfromInternet(query)
        if testFlag==True:
            print "File Not Exist,Create File"
        if weatherDictionary[query][1]==[]:
            return -1
        else:
            writeToLocalDB(weatherDictionary)
            return weatherDictionary[query][1]             
    else:#If file has been created before, this block will be executed
        weatherDictionary=pickle.load(databaseFile)   
        if(query in weatherDictionary):

            if (time.time()-weatherDictionary[query][0] > expirationTime):  #Default=6Hours 6*60*60 Seconds!
                if testFlag==True:
                    print "Data was expired,Reading new data From Internet"
                temp=readfromInternet(query)
                if temp[query][1]==[]:
                    return -1
                else:                    
                    weatherDictionary[query]=temp[query]
                    databaseFile.close()
                    writeToLocalDB(weatherDictionary)
                    return weatherDictionary[query][1] 
            if testFlag==True:
                print "Data found on history,Reading From a Disk"                    
            #print weatherDictionary[query][1]
            return weatherDictionary[query][1]
        else:
            if testFlag==True:
                print "New data has been added to history"
            temp=readfromInternet(query)
            if temp[query][1]==[]:
                return -1                
            else:
                weatherDictionary[query]=temp[query]
                databaseFile.close()
                writeToLocalDB(weatherDictionary)
                return weatherDictionary[query][1]
                                                 
def secondsToDate(seconds):
    return datetime.datetime.fromtimestamp(float(seconds)).strftime("%Y-%m-%dT%H:%M:%S")
def dateToSeconds(date):
    return date.strftime("%s")
def stringToDate(dateString):
    return datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S")
  

def weather_update_retrieve(location,selectedHour,selectedMinute):
    location=re.sub(u"[\s]+",u" ",location)
    currentTime=datetime.datetime.now()
    token=False
    timeForPredicate=dateToSeconds(currentTime.replace(hour=selectedHour,minute=selectedMinute))
    if  timeForPredicate<dateToSeconds(currentTime):
        timeForPredicate=float(timeForPredicate)+(24*60*60)
    temp=[]
    try:
        for urls in readFromLocalDB(location):    
            try:                                             
                if token==False:
                    #print datetime.datetime.fromtimestamp(float(timeForPredicate)).strftime("%d.%m.%y %H:%M")
                    temp.append(datetime.datetime.fromtimestamp(float(timeForPredicate)).strftime("%d.%m.%y %H:%M"))
                    token=True
                for timeSlots in readFromLocalDB(urls)[1]:
                    startSlot=dateToSeconds(stringToDate(timeSlots[0]))
                    endSlot=dateToSeconds(stringToDate(timeSlots[1]))            
                    if float(timeForPredicate) >=float(startSlot) and float(timeForPredicate) <=float(endSlot):                    
                        #print u"{0}: {1}, rain:{2} mm, wind:{3} mps, temp:{4} deg C".format(readFromLocalDB(urls)[0][0],timeSlots[2],timeSlots[3],timeSlots[4],timeSlots[5])
                        temp.append([readFromLocalDB(urls)[0][0],timeSlots[2],timeSlots[3],timeSlots[4],timeSlots[5]])
                        break                                                 
            except:
                print u"This link was not found: {0}".format(urls) 
        return temp
    except:
        print "Not match found"
def weather_update(location,selectedHour,selectedMinute):
    temp=weather_update_retrieve(location,selectedHour,selectedMinute)
    if temp:
        print temp[0]
        for placeWeatherInfo in temp[1:]:
            print u"{0:<25} {1:<20} rain:{2:>7}    wind:{3:>7}    temp:{4:3} deg C".format(placeWeatherInfo[0],placeWeatherInfo[1],placeWeatherInfo[2]+u"mm",placeWeatherInfo[3]+u"mps",placeWeatherInfo[4])

def extremePlaces():
    listOfPlaces=weather_update_retrieve("",13,0)[1:]
    result = u"\n".join(u"\t".join(l) for l in listOfPlaces)
    listOfTemperature=re.findall(u"^.*?\\t(\\d+)$",result,re.MULTILINE)    
    listOfTemperature=[int(item.decode("utf-8")) for item in listOfTemperature]
    maxTemperature=max(listOfTemperature)
    minTemperature=min(listOfTemperature)
    print weather_update_retrieve("",13,0)[0]
    for item in listOfPlaces:
        if maxTemperature==int(item[4]):
            print u"Hot city: {0:<25}                Temperature: {1}".format(item[0],item[4])
    for item in listOfPlaces:
        if minTemperature==int(item[4]):
            print u"Cold city: {0:<25}                Temperature: {1}".format(item[0],item[4])
