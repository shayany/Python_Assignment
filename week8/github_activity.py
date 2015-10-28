from subprocess import Popen, PIPE
import argparse
import time
from datetime import datetime
import os
import re
from matplotlib import pyplot
from IPython import embed
from datetime import timedelta
from numpy import *
import matplotlib.cm as cm
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
    gitlog = Popen(["git","log"], stdout=PIPE).communicate()[0]
    Author = re.findall(u"^Author: (.*?) <.*>$",gitlog,re.IGNORECASE|re.MULTILINE)
    Date = re.findall(u"^Date:[\s]{3}(?:.*?) (.*?) (.*?) \d+\d+:\d+\d+:\d+\d+ (.*?) (?:.*)$",gitlog,re.IGNORECASE|re.MULTILINE)
    mydic={}
    for item in zip(Author,Date):
        if str(item[0]) not in mydic:
            mydic[str(item[0])]={datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')"):1}            
        else:
            if datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')") in mydic[str(item[0])]:
                mydic[str(item[0])][datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')")]+=1
            else:
                mydic[str(item[0])][datetime.strptime(str(item[1]),r"('%b', '%d', '%Y')")]=1
    #embed()
    userCollection={}
    for user in mydic:
        commitDate=[]
        numberOfCommits=[]        
        for day in mydic[user]:
            commitDate.append(day)
            numberOfCommits.append(mydic[user][day])

        temp=zip(commitDate,numberOfCommits)
        temp.sort()
        commitDate=list(zip(*temp)[0])
        numberOfCommits=list(zip(*temp)[1])
        #if args.plot:
        #    fig=pyplot.figure() 
        """       
        pyplot.plot_date(x=commitDate, y=numberOfCommits,fmt="-o")
        pyplot.title("Histogram of {}\'s commits".format(user))
        pyplot.yticks(range(0,max(numberOfCommits)+1))
        #pyplot.fill_between(interpolate=True, color='blue')  
        pyplot.show()
        """
        userCollection[user]={'date':commitDate,'number':numberOfCommits}
        #if args.plot:
        #    fig.savefig(user+str(time.time())+".png")

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
        #dateAxis.append(day.isoformat())
        dateAxis.append(day)
        for i in range (len(userCollection)):
            localVariables['user_{0}'.format(i)].append(datedic[day][i])

#colors=['b','g','r','c','m','y','k','w']
    cmap = pyplot.get_cmap('gnuplot')
    colors = cm.rainbow(linspace(0, 1, len(userCollection)))
    clrIndex=0

    for i in range(len(userCollection)):
        localVariables['user_{0}'.format(i)]=array(localVariables['user_{0}'.format(i)])

    b=0
    users=[str(i) for i in userCollection]
    if args.plot:
        fig=pyplot.figure() 
    for i in range(0,len(userCollection)):
        if i==0:
            b=0
        else:        
            b+=array(localVariables['user_{0}'.format(i-1)])
        #print colors[clrIndex]
        pyplot.bar(dateAxis,localVariables['user_{0}'.format(i)],color=colors[clrIndex],bottom=b,label=users[i])
        clrIndex+=1
    b+=array(localVariables['user_{0}'.format(len(userCollection)-1)])
    #pyplot.bar(dateAxis,user_0,color='r',bottom=0)
    #pyplot.bar(dateAxis,user_1,color='y',bottom=user_0)
    #pyplot.bar(dateAxis,user_2,color='g',bottom=user_0+user_1)
    #pyplot.bar(dateAxis,user_3,color='b',bottom=user_0+user_1+user_2)
    pyplot.yticks(arange(0, (b).max(), 1))
    pyplot.xticks(rotation='vertical')
    pyplot.legend()
    if args.plot:
        fig.savefig(str(time.time())+".png",format='png', dpi=1200)
    pyplot.show()


            
        
    
    
