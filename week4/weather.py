# -*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8
from subprocess import Popen,PIPE
import re
import urllib
def getContent(url):
    """
    Return contents of the URL.
    """
    return str(urllib.urlopen(url).read())
    #stringmy =Popen("curl http://fil.nrk.no/yr/viktigestader/noreg.txt",stdout=PIPE).communicate()[0]
    #print stringmy

def findLink(name):
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
    plainTextFile=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt") #Get content from this URL
    noregTable=plainTextFile.split("\r\n") #Split the lines into the list 
    xmlList=[]#Create Empty list to return results 
    name=name.replace("?",u".?")    #Replace wildcards (this is the format that regex support) 
    name=name.replace("*",u".*")    #Replace wildcards (this is the format that regex support) 
    
    for counter in range(len(noregTable)-1):
        noregTable[counter]=noregTable[counter].split("\t") #Split each line to a list of fields 
        if re.findall(r"(?i)^{0}$".format(name.encode("utf-8")),str(noregTable[counter][1]).decode("utf-8")):
            if not str(noregTable[counter][13]).decode("utf-8") in xmlList: 
                xmlList.append(str(noregTable[counter][13]).decode("utf-8"))                      
    if not xmlList:
        for counter in range(len(noregTable)-1):
            if re.findall(r"(?i)^{0}$".format(name.encode("utf-8")),str(noregTable[counter][6]).decode("utf-8")):
                if not str(noregTable[counter][13]).decode("utf-8") in xmlList: 
                    xmlList.append(str(noregTable[counter][13]).decode("utf-8"))                    
        if xmlList:
            return xmlList
    if not xmlList:
        for counter in range(len(noregTable)-1):
            if re.findall(r"(?i)^{0}$".format(name.encode("utf-8")),str(noregTable[counter][7]).decode("utf-8")):
                if not str(noregTable[counter][13]).decode("utf-8") in xmlList: 
                    xmlList.append(str(noregTable[counter][13]).decode("utf-8"))               
        if xmlList:
            return xmlList
    if name=="":
        for counter in range(len(noregTable)-1):
            if not str(noregTable[counter][13]).decode("utf-8") in xmlList: 
                xmlList.append(str(noregTable[counter][13]).decode("utf-8"))               
        if xmlList:
            return xmlList
    return xmlList 

#Query example       
for item in findLink(""):
    print item.encode("utf-8")
