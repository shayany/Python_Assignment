def helpCommands(command):
    """
    Get python command with question mark ? and show the result
    """
    command=command.split()
    temp=command[len(command)-1]
    help(temp[:-1])