# -*- coding: utf-8 -*-
from weather import getContent,findLink,weatherInformation,readFromLocalDB
import urllib
import re
import time
import os

def test_contentOftheURL():
    assert getContent("http://www.islostarepeat.com/")==str(urllib.urlopen("http://www.islostarepeat.com/".encode("utf-8")).read()).decode("utf-8")
def test_checkURLAddress():
    assert findLink(u"Hannestad")[0]==u"http://www.yr.no/place/Norway/Østfold/Sarpsborg/Hannestad/forecast.xml".lower()
def test_temperature():
    assert float(weatherInformation(findLink("Hannestad")[0])[1][0][5])>=-50 and float(weatherInformation(findLink("Hannestad")[0])[1][0][5])<=+50

def test_buffer(capsys):
    if os.path.isfile("weatherDB.log"):
        os.remove("weatherDB.log")        
    capsys.readouterr()
    readFromLocalDB(u"oslo",10,True)
    out,err=capsys.readouterr()
    assert out=="File Not Exist,Create File\n"
    time.sleep(5)
    capsys.readouterr()    
    readFromLocalDB(u"oslo",10,True)
    out,err=capsys.readouterr()
    assert out=="Data found on history,Reading From a Disk\n"
    time.sleep(5)
    readFromLocalDB(u"oslo",10,True)
    out,err=capsys.readouterr()
    assert out=="Data was expired,Reading new data From Internet\n"
    time.sleep(5)
    readFromLocalDB(u"oslo",10,True)
    out,err=capsys.readouterr()
    assert out=="Data found on history,Reading From a Disk\n"
    time.sleep(5)
    readFromLocalDB(u"oslo",10,True)
    out,err=capsys.readouterr()
    assert out=="Data was expired,Reading new data From Internet\n"
    readFromLocalDB(u"halden",10,True)
    out,err=capsys.readouterr()
    assert out=="New data has been added to history\n"

def test_replaceExpiredFile(capsys):
    
    if os.path.isfile("weatherDB.log"):
        os.remove("weatherDB.log")  
    capsys.readouterr()
    readFromLocalDB(u"oslo",5,True)
    creation=os.path.getctime("weatherDB.log")
    time.sleep(5)
    readFromLocalDB(u"oslo",5,True)
    modifiedTime=os.path.getmtime("weatherDB.log")
    assert creation+5<modifiedTime
    
def test_DoesNotreplaceFile(capsys):    
    if os.path.isfile("weatherDB.log"):
        os.remove("weatherDB.log")
    capsys.readouterr()
    readFromLocalDB(u"oslo",21600,True)#Expire after 6 hours
    creationTime=os.path.getctime("weatherDB.log") #This function return time of creation
    time.sleep(5)
    readFromLocalDB(u"oslo",21600,True)
    modifiedTime=os.path.getmtime("weatherDB.log") #This function return time of modification
    assert modifiedTime==creationTime