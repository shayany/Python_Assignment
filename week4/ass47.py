import re
from ass45 import weather_update_retrieve

def extremePlaces():
    """
    This function shows the hottest and coldest places in Norway
    
    """
    try:
        listOfPlaces=weather_update_retrieve("",13,0)[1:]        #Get weather information for all the places      
        result = u"\n".join(u"\t".join(l) for l in listOfPlaces)    #Join list of list for using regex
        listOfTemperature=re.findall(u"^.*?\\t(\\d+)$",result,re.MULTILINE)    #Make a list of all temperatures
        listOfTemperature=[int(item.decode("utf-8")) for item in listOfTemperature] 
        maxTemperature=max(listOfTemperature)
        minTemperature=min(listOfTemperature)
        print weather_update_retrieve("",13,0)[0]                #Print timeStamp
        for item in listOfPlaces:
            if maxTemperature==int(item[4]):
                print u"Hot city: {0:<25}                Temperature: {1}".format(item[0],item[4])
        for item in listOfPlaces:
            if minTemperature==int(item[4]):
                print u"Cold city: {0:<25}                Temperature: {1}".format(item[0],item[4])
    except:
        print "Can not read"
