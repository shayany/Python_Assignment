"""
It shows a contribution histogram from provided github filepath

It return message in case of error

The plot image will be saved in github directory
"""

from subprocess import Popen, PIPE
import argparse
import time
from datetime import datetime
import os
import re
from matplotlib import pyplot

from datetime import timedelta
from numpy import *
import matplotlib.cm as cm

def CommitLog(gitpath):
    os.chdir(gitpath)
    gitlog = Popen(["git","log"], stdout=PIPE).communicate()[0]
    Author = re.findall(u"^Author: (.*?) <.*>$",gitlog,re.IGNORECASE|re.MULTILINE)#Use Regex to capture authors
    Date = re.findall(u"^Date:[\s]{3}(?:.*?) (.*?) (.*?) \d+\d+:\d+\d+:\d+\d+ (.*?) (?:.*)$",gitlog,re.IGNORECASE|re.MULTILINE)#Use Regex to capture dates of commits
    
    authorDateDictionary={}#In this dictionary I will save the Authors and number of commits per each date for each authors!
    for item in zip(Author,Date):
        if str(item[0]) not in authorDateDictionary:
            authorDateDictionary[str(item[0])]={datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')"):1}            
        else:
            if datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')") in authorDateDictionary[str(item[0])]:
                authorDateDictionary[str(item[0])][datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')")]+=1
            else:
                authorDateDictionary[str(item[0])][datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')")]=1
    return authorDateDictionary



parser = argparse.ArgumentParser()
parser.add_argument("input", help="Filepath")
parser.add_argument("--plot", help="save the plots",action="store_true")

args = parser.parse_args()
 
try:
    os.chdir(args.input)
    stdout_string = Popen(["git","rev-parse","--git-dir"], stdout=PIPE).communicate()[0]
    if stdout_string=="":
        raise Exception
except:
    print "Invalid filepath"    
else:

    print "This is a github repository"
    authorDateDictionary=CommitLog(args.input)
    userCollection={}
    for user in authorDateDictionary:
        commitDate=[]
        numberOfCommits=[]        
        for day in authorDateDictionary[user]:
            commitDate.append(day)
            numberOfCommits.append(authorDateDictionary[user][day])
        temp=zip(commitDate,numberOfCommits)
        temp.sort()
        commitDate=list(zip(*temp)[0])
        numberOfCommits=list(zip(*temp)[1])
        userCollection[user]={'date':commitDate,'number':numberOfCommits}


    minDate=datetime.now()
    maxDate=datetime(1900,1,1)

    for i in userCollection:
        if min(userCollection[i]['date'])<minDate:
            minDate=min(userCollection[i]['date'])
        if max(userCollection[i]['date'])>maxDate:
            maxDate=max(userCollection[i]['date'])

    datedic={}

    for i in range((maxDate-minDate).days):    
        datedic[minDate]=[]    
        minDate+=timedelta(days=1)
    for day in datedic:
        temp=[]
        for user in userCollection:
            try:
                temp.append(userCollection[user]['number'][userCollection[user]['date'].index(day)]) 
            except:
                temp.append(0)
        datedic[day]=temp
    
    localVariables = locals()
    dateAxis=[]
    for i in range(0,len(userCollection)):
        localVariables['user_{0}'.format(i)] = []
    

    for day in sorted(datedic):    
        dateAxis.append(day)
        for i in range (len(userCollection)):
            localVariables['user_{0}'.format(i)].append(datedic[day][i])

    cmap = pyplot.get_cmap('gnuplot')
    colors = cm.rainbow(linspace(0, 1, len(userCollection)))
    clrIndex=0

    for i in range(len(userCollection)):
        localVariables['user_{0}'.format(i)]=array(localVariables['user_{0}'.format(i)])

    sumOfCommits=0 
    users=[str(i) for i in userCollection]
    if args.plot:
        fig=pyplot.figure()
         
    for i in range(0,len(userCollection)):
        if i==0:
            sumOfCommits=0
        else:        
            sumOfCommits+=array(localVariables['user_{0}'.format(i-1)])
        pyplot.bar(dateAxis,localVariables['user_{0}'.format(i)],color=colors[clrIndex],bottom=sumOfCommits,label=users[i])
        clrIndex+=1
        
    sumOfCommits+=array(localVariables['user_{0}'.format(len(userCollection)-1)])
    pyplot.yticks(arange(0, (sumOfCommits).max(), 1))
    pyplot.xticks(rotation='vertical')
    pyplot.legend()
    if args.plot:
        fig.savefig(str(time.time())+".png",format='png', dpi=1200)
    pyplot.show()


            
        
    
    
