from subprocess import Popen, PIPE
import argparse
import time
from datetime import datetime
import os
import re
from matplotlib import pyplot
#from IPython import embed embed()

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
        if args.plot:
            fig=pyplot.figure()        
        pyplot.plot_date(x=commitDate, y=numberOfCommits,fmt="-o")
        pyplot.title("Histogram of {}\'s commits".format(user))
        pyplot.yticks(range(0,max(numberOfCommits)+1))
        #pyplot.fill_between(interpolate=True, color='blue')  
        pyplot.show()
        if args.plot:
            fig.savefig(user+str(time.time())+".png")

            
        
    
    