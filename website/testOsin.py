import website.Osintgram as osint

targetID = input("ENTER TARGET : ")
file = True
json = True
output = 'output'
cookies = True
command = False

api = osint.Osintgram(targetID, file, json, command, output, cookies)

addresses = api.get_addrs()

