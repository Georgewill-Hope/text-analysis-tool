# Welcome user
def welcomeUser():
    print("\nWelcome to the analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    # Print message prompting user to input their name
    username = input("\nTo begin, please enter your username:\n")

    return username   

# Greet the user
def greetUser(name):
    print("Hello, " + name)

welcomeUser()
username = getUsername()
greetUser(username)