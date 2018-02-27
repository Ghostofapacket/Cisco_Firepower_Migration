#!/usr/bin/python
# =====================================================================================================================
#
# Overview: This script delete objects out of Cisco FMC utilizing the built-in API
#
# Usage:    Run python <script_name>
#
# Use script at you own risk, and no warranties are inferred or granted.
#
# Originally written by jwilliams9999: https://github.com/jwilliams9999/fmcapi/blob/master/fmc-obj-del.py
#
# Modified to be more interactive and python3 compatable by Matt Iggo
# Github URL: https://github.com/MattIggo/Cisco_Firepower_Migration/
#
# =====================================================================================================================

import requests
import json
import requests
import logging
import sys
import msvcrt
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import init,Fore,Back,Style
init()

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(filename='response.log', level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.INFO)
requests_log.propagate = True

set_echo = '#' # Setting the symbol for encryption which will going to be displayed.

def getpass(label):
    print(label, end='')
    passwor = ''
    while True:
        inp = msvcrt.getch()
        if bytes.decode(inp) == '\r':
            if passwor == '':
                print(label)
            else:
                break
        elif inp == '\b':
            print("\x1b[2K\x1b[1A")
            del passwor
            passwor = ''
            print(label)
        elif bytes.decode(inp) == '\003':
            raise KeyboardInterrupt
        elif bytes.decode(inp) == '\x03':
            raise KeyboardInterrupt
        elif bytes.decode(inp) == '\04':
            raise EOFError
        else:
            sys.stdout.write(set_echo)
            #print(inp)
            #print(bytes.decode(inp))
            convertedkeypress = bytes.decode(inp)
            passwor += convertedkeypress
    #print("\n",)
    return passwor

# Begin user presentation / Input
#Make the output bright!
print(Style.BRIGHT)
print("======================================")
print("=      Cisco Firepower API           =")
print("=      Object Delete script          =")
print("=  Will only delete unused objects   =")
print('=     ' + Fore.LIGHTRED_EX + 'Use at your own Risk!'+ Fore.WHITE+'          =')
print("=       Version: 1.0.2               =")
print("=      Updated by Matt Iggo          =")
print("======================================")

# Interactive Input of FMC and login
user1 = input("Enter your FMC api username: ")
#pass1 = input("Enter your FMC password: ")
pass1 = getpass("Enter your FMC password: ")
print("\n")
ipaddr = input("Enter the IP address of Firepower Management Center: ")
print("Enter the object type to delete?")
print("1. networks")
print("2. ports")
print("3. hosts")
print("4. network groups")
print("5. port groups")
print("6. address ranges")
#print("Q to quit")
while True:
    try:
        question = int(input('Options (1,2,3,4,5,6):'))

    except ValueError:
        print("Sorry, that is an invaild option.")
        # better try again... Return to the start of the loop
        continue

    if question == 1:
        fmcobj = 'networks'
        break

    elif question == 2:
        fmcobj = 'ports'
        break

    elif question == 3:
        fmcobj = 'hosts'
        break

    elif question == 4:
        fmcobj = 'networkgroups'
        break

    elif question == 5:
        fmcobj = 'portobjectgroups'
        break

    elif question == 6:
        fmcobj = 'ranges'
        break

    elif question == "Q":
        sys.exit()
        break

    else:
        print('That\'s not an option!')
        continue
print(Style.RESET_ALL)

url = "https://%s/api/fmc_platform/v1/auth/generatetoken" % ipaddr

results = []

headers = {
    'cache-control': "no-cache",
    'postman-token': "ff30c506-4739-9d4d-2e53-0dc7efc2036a"
}

response = requests.request("POST", url, headers=headers, auth=(user1, pass1), verify=False)

# Authenicates token used in addiotnal HTTPS CRUD request
auth = response.headers['X-auth-access-token']

url = "https://%s/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/%s" % (ipaddr, fmcobj)

querystring = {"limit": "1000"}

headers = {
    'x-auth-access-token': auth,
    'cache-control': "no-cache",
    'postman-token': "ff30c506-4739-9d4d-2e53-0dc7efc2036a"
}

# get all objects type based in user reponse from FMC
response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
results = []
raw = response.json()
offset = 0

if raw['paging']['pages'] == 0:
    for pages in range(p):
        querystring = {"offset": "%d" % offset, "limit": "1000"}
        response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
        offset += 1000
        raw = response.json()
        # print [raw[i] for i in raw.keys()]
        # print raw['items'][1]['name']
        # print [raw[i][0][0].get('name') for i in raw.keys()]
        for i in raw['items']:
            results.append(i)

else:
    p = raw['paging']['pages']
    # FMC get all objects for user specified type
    for pages in range(p):
        querystring = {"offset": "%d" % offset, "limit": "1000"}
        response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
        offset += 1000
        raw = response.json()
        # print [raw[i] for i in raw.keys()]
        # print raw['items'][1]['name']
        # print [raw[i][0][0].get('name') for i in raw.keys()]
        for i in raw['items']:
            results.append(i)


# test of results link
# for i in results:
#   print i['links']['self']

def delobj(obj):
    global response
    global headers
    global ipaddr
    global user1
    global pass1
    netdel = response

    for id in obj:

        # Sends a delete http for all network objects, but only deletes unused objects

        if netdel.status_code != 401:
            url = id['links']['self']
            netdel = requests.request("DELETE", url, headers=headers, verify=False)
            #print(id['name'], netdel)
            if str(netdel) == "<Response [200]>":
                print(id['name'], "object deletion " + Fore.LIGHTGREEN_EX + "success!" + Style.RESET_ALL)
            else:
                print(id['name'], "object deletion " + Fore.LIGHTRED_EX + "FAILURE!", Fore.LIGHTCYAN_EX + str(netdel) +
                      Style.RESET_ALL)
            logging.info("%s Response: Status code: %d" % (id['name'], netdel.status_code))

        else:
            urlauth = "https://%s/api/fmc_platform/v1/auth/generatetoken" % ipaddr
            headers = {
                'cache-control': "no-cache",
                'postman-token': "ff30c506-4739-9d4d-2e53-0dc7efc2036a"
            }
            response = requests.request("POST", urlauth, headers=headers, auth=(user1, pass1), verify=False)
            # Authenicates token used in addiotnal HTTPS CRUD request
            auth = response.headers['X-auth-access-token']
            headers = {
                'x-auth-access-token': auth,
                'cache-control': "no-cache",
                'postman-token': "ff30c506-4739-9d4d-2e53-0dc7efc2036a"
            }

            netdel.status_code = 200


delobj(results)
