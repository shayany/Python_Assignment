def helpCommands(command):
    """
    Get python command with question mark ? and return the result
    """
    command=command.split()
    temp=command[len(command)-1]
    print temp
    return help(temp[:-1])