from subprocess import Popen, PIPE
from os import system
def OS_Commands(command):
    """
    Get operating system command and return the result
    """
    command=command[1:]#Remove exclamation
    try:
        listOfCommands=command.split()
        commandOutput = Popen(listOfCommands, stdout=PIPE).communicate()[0]
    except:
        system(command)
        commandOutput = Popen(["ls"], stdout=PIPE).communicate()[0]        
    return commandOutput