class SimpleString(object):
    """
    This class has two functions :
    1-getString: to get a string from console input
    2-printString: to print the string in upper case
    """
    def getString(self):
        """
        This function get string value from a terminal 
        and save that value in a local variable which called
        userInput
        """
        self.userInput = raw_input()
    def printString(self):
        """
        Print value of the self.userInput on terminal
        """
        print self.userInput.upper()
