# In Python2.7, the way to take user input is with raw_input()

def myName():
    # Set a variable 'name' to equal the user input after the prompt, "What is you name?".
    name = raw_input("What is your name?")
    print "Hello, "+name


myName()