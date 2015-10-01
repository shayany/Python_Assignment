import datetime
import re
from weather import readFromLocalDB                                                


def secondsToDate(seconds):
    """
    This function get seconds and convert it into datetime object according to pattern
    """
    return datetime.datetime.fromtimestamp(float(seconds)).strftime("%Y-%m-%dT%H:%M:%S")


def dateToSeconds(date):
    """
    This function get datetime and return number os seconds
    """
    return date.strftime("%s")

def stringToDate(dateString):
    """
    This function convert the string to datetime object according to pattern
    """
    return datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S")
  



def weather_update_retrieve(location,selectedHour,selectedMinute):
    """
    Return list of list that includes all the weather information for specific location
    ['DD.MM.YY HH:MM', [CITY, SYMBOL, PRECIPITATION, WINDSPEED, TEMPERATURE]]
    """
    location=re.sub(u"[\s]+",u" ",location)#Remove Extra space from query
    currentTime=datetime.datetime.now()
    token=False#Use this flag to add a timestamp to my list just for the first iteration
    timeForPredicate=dateToSeconds(currentTime.replace(hour=selectedHour,minute=selectedMinute))
    if  timeForPredicate<dateToSeconds(currentTime):
        timeForPredicate=float(timeForPredicate)+(24*60*60)
    temp=[]
    try:
        for urls in readFromLocalDB(location):    
            try:                                             
                if token==False:
                    temp.append(datetime.datetime.fromtimestamp(float(timeForPredicate)).strftime("%d.%m.%y %H:%M"))
                    token=True
                for timeSlots in readFromLocalDB(urls)[1]:
                    startSlot=dateToSeconds(stringToDate(timeSlots[0]))
                    endSlot=dateToSeconds(stringToDate(timeSlots[1]))            
                    if float(timeForPredicate) >=float(startSlot) and float(timeForPredicate) <=float(endSlot):                    
                        temp.append([readFromLocalDB(urls)[0][0],timeSlots[2],timeSlots[3],timeSlots[4],timeSlots[5]])
                        break                                                 
            except:
                print u"This link was not found: {0}".format(urls) 
        return temp
    except:
        print "Not match found"
        
        
        
def weather_update(location,selectedHour,selectedMinute):
    """
    Print table of weather information for specific location
    
    Parameters
    __________
    location :Name of place
    SelectedHour: Hour of forecast
    selectedMinute: Minute of forecast
    """
    if type(location)!=unicode:
        location=location.decode("utf-8") 
    weatherInfoTable=weather_update_retrieve(location,selectedHour,selectedMinute)
    if weatherInfoTable:
        print weatherInfoTable[0]                    #Print time of forecast
        for placeWeatherInfo in weatherInfoTable[1:]:
            print u"{0:<25} {1:<20} rain:{2:>7}    wind:{3:>7}    temp:{4:3} deg C".format(placeWeatherInfo[0],placeWeatherInfo[1],placeWeatherInfo[2]+u"mm",placeWeatherInfo[3]+u"mps",placeWeatherInfo[4])


