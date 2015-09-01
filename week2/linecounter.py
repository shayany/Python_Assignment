from sys import argv
listOfFiles=argv[1:]
for item in listOfFiles:
    file=open(item,"r")
    numberOfLine=0
    for l in file:
        numberOfLine=numberOfLine+1
    print item+": "+str(numberOfLine)
    file.close()

