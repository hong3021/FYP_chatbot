import configparser
import sys

try:
    config = configparser.ConfigParser(interpolation=None)
    # config.read("src/credentials.ini")
    config.read("website/src/credentials.ini")
except FileNotFoundError:
    print('Error: file "credentials.ini" not found!\n')
    sys.exit(0)
except Exception as e:
    print("Error: {}\n".format(e))
    sys.exit(0)


def getUsername():
    try:

        username = config["Credentials"]["username"]

        if username == '':
            print('Error: "username" field cannot be blank in "credentials.ini"\n')
            sys.exit(0)

        return username
    except KeyError:
        print('Error: missing "username" field in "credentials.ini"\n')
        sys.exit(0)

def getPassword():
    try:

        password = config["Credentials"]["password"]

        if password == '':
            print('Error: "password" field cannot be blank in "credentials.ini"\n')
            sys.exit(0)

        return password
    except KeyError:
        print('Error: missing "password" field in "credentials.ini"\n')
        sys.exit(0)
