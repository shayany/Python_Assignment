from sys import argv
listOfFiles=argv[1:]
for item in listOfFiles:
    file=open(item,"r")
    numberOfWords=0
    for l in file:
        temp=l.split()
        numberOfWords=numberOfWords+len(temp)
    print item+": "+str(numberOfWords)
    file.close()
