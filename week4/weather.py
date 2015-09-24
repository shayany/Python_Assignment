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
    return str(urllib.urlopen(url).read()).decode("utf-8")
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
    plainTextFile=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt") #Get content from this URL
    xmlList=[]#Create Empty list to return results 
    cityName=name.decode("utf-8").replace("?","[^\\t]?")    #Replace wildcards (this is the format that regex support) 
    cityName=cityName.replace("*","[^\\t]*?")    #Replace wildcards (this is the format that regex support) 
    """
    if name=="":    
        xmlList = re.findall("^.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
        return list(set(xmlList))               
    """
    xmlList = re.findall(u"^\\d*\\t{0}\\t.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
    if xmlList:
        return list(set(xmlList))   
    
    if not xmlList:
        xmlList = re.findall(u"^\\d*\\t.*?\\t.*?\\t.*?\\t.*?\\t.*?\\t{0}\\t.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
        if xmlList:
            list(set(xmlList))    
    if not xmlList:
        xmlList = re.findall(u"^\\d*\\t.*?\\t.*?\\t.*?\\t.*?\\t.*?\\t.*?\\t{0}\\t.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
        if xmlList:
            list(set(xmlList))   
    return list(set(xmlList))

def weatherInformation(url):
    content=getContent(url)
    #print type(content)
    #print content.encode("utf-8")
    tabular=re.findall(u"<tabular>((\\s|\\r|\\n|.)*?)</tabular>",content.encode("utf-8"),re.I+re.MULTILINE)
    print type(str(tabular[0]))
#Query example       
for item in findLink("Vestfold"):
    print item.encode("utf-8")



#weatherInformation(findLink("?s?land?")[0].encode("utf-8"))


