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
    if not(str.isalpha(name) or "*" in name or "?" in name or not name or " " in name):
        raise  ValueError,"Enter only letters or wildcards(* or ?)"
    plainTextFile=getContent("http://fil.nrk.no/yr/viktigestader/noreg.txt") #Get content from this URL
    xmlList=[]#Create Empty list to return results 
    cityName=name.decode("utf-8").replace("?","[^\\t]?")    #Replace wildcards (this is the format that regex support) 
    cityName=cityName.replace("*","[^\\t]*?")    #Replace wildcards (this is the format that regex support) 

    if name=="":    
        xmlList = re.findall("^.*\\t(.*?)\\r$".format(cityName),plainTextFile,re.I+re.MULTILINE)
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
        if xmlList:
            list(set(xmlList))   
    return list(set(xmlList))

def weatherInformation(url):
    content=getContent(url)
    locationName=re.findall(u"<[^.]*?name[^.]*?>(.*?)<[^.]*?/[^.]*name[^.]*?>",content,re.I+re.MULTILINE)
#    <[^.]*?name[^.]*?>(.*?)<[^.]*?/[^.]*name[^.]*?>
    weatherContent=re.findall(u"<tabular>(.*?)</tabular>",content,re.I+re.MULTILINE+re.DOTALL)[0]
    timeContent=re.findall((u"<time from=\"(.*?)\" to=\"(.*?)\" period=\"(?:.*?)\">"
                            ".*?<symbol.*?name=\"(.*?)\".*?>.*?"
                            "<precipitation value=\"(.*?)\".*?>.*?"
                            "<windSpeed mps=\"(.*?)\".*?>.*?"
                            "<temperature unit=\"(?:.*?)\" value=\"(.*?)\".*?>")
                            ,weatherContent,re.I+re.MULTILINE+re.DOTALL)
#    timeContent=re.findall(u"<time from=\"(.*?)\" to=\"(.*?)\" period=\"(?:.*?)\">.*?<symbol.*?name=\"(.*?)\".*?>.*?<precipitation value=\"(.*?)\".*?>.*?<windSpeed mps=\"(.*?)\".*?>.*?<temperature unit=\"(?:.*?)\" value=\"(.*?)\".*?>",weatherContent[0],re.I+re.MULTILINE+re.DOTALL)
    return locationName,timeContent
    #time=re.findall(u"(<time.*?/time>)",weathercontent,re.I+re.MULTILINE+re.DOTALL)
    #print type(content)
    #print content.encode("utf-8")
    #tabular=re.findall(u"<tabular>((\\s|\\r|\\n|.)*?)</tabular>",content.encode("utf-8"),re.I+re.MULTILINE)
    #print type(str(tabular[0]))
#Query example       
#for item in findLink("?s*land?"):
#    print item.encode("utf-8")
print weatherInformation(findLink("nordsinni")[0].encode("utf-8"))