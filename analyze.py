from random_username.generate import generate_username

# Welcome user
def welcomeUser():
    print("\nWelcome to the analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    # Print message prompting user to input their name
    usernameFromInput = input("\nTo begin, please enter your username:\n")

    if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
        print("Your username must be at least 5 character long, alphanumeric only (a-z/A-Z/0-9), have no spaces and cannot start with a number")
        usernameFromInput = generate_username()[0]
        print("Assigning username instead...")


    return usernameFromInput   

# Greet the user
def greetUser(name):
    print("Hello, " + name)

welcomeUser()
username = getUsername()
greetUser(username)