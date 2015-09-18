# -*- coding: utf-8 -*-
from subprocess import Popen,PIPE
import re
import urllib
def getContent(url):
    """
    Return contents of the URL.
    """
    return urllib.urlopen(url).read()
    #return Popen("curl "+url,stdout=PIPE).communicate()[0]

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
    plainTextFile=getContent(u"http://fil.nrk.no/yr/viktigestader/noreg.txt");
    noregTable=plainTextFile.split("\r\n");
    xmlList=[]
    #reTemplate=re.template(name)
    for counter in range(len(noregTable)-1):
        noregTable[counter]=noregTable[counter].split("\t")
        if re.findall(r"^\bSv.*\b",noregTable[counter][1]):
            xmlList.append(noregTable[counter][1])
    print xmlList