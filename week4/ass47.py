import re
from weather import weather_update_retrieve
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
