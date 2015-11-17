
def saveCommandsHistory(listOfCommands,fileName):
    """
    Get list of the commands and save them in current directory based on the file name
    """
    temp=""
    for i in listOfCommands:
        temp+=i+"\r\n"
    f=open(fileName,"w")
    f.write(temp)
    f.close()