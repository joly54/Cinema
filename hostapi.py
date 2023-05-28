import os

import requests
import config
import easygui

api_base_url = "https://www.pythonanywhere.com/api/v0/user/vincinemaApi"
api_token = config.api_token

consindex = -1
consoles = []


def GetConsoles(param=1):
    global consindex, consoles
    response = requests.get(api_base_url + "/consoles/", headers={"Authorization": "Token " + api_token})
    if response.status_code == 200:
        consoles = response.json()
        print("Select console:")
        for i in range(len(consoles)):
            print(f"{i + 1}. {consoles[i]['name']}")
        if param == 1:
            while True:
                try:
                    consindex = int(input("Enter console index: "))
                    if consindex > len(consoles) or consindex < 1:
                        print("Error: Invalid console index.")
                    else:
                        consindex -= 1
                        break
                except ValueError:
                    print("Error: Invalid console index.")
    else:
        print("Error: Could not retrieve console data.")
        exit()


GetConsoles()


def GetOutput():
    response = requests.get(api_base_url + "/consoles/{id}/get_latest_output/".format(id=consoles[consindex]["id"]),
                            headers={"Authorization": "Token " + api_token})
    if response.status_code == 200:
        os.system("cls")
        print(f"{response.json()['output']}", end="")
    else:
        print("Error: Could not retrieve console output.\n" + str(response.json()))


def SendInput(text):
    print("waiting for response...")
    response = requests.post(api_base_url + "/consoles/{id}/send_input/".format(id=consoles[consindex]["id"]),
                             data={"input": text + "\n"}, headers={"Authorization": "Token " + api_token})
    print(response.text)
    if response.status_code != 200:
        print("Error: Could not send input to console.")


is_reloading = False
import time
import threading


def print_time():
    curent_time = time.time()
    while is_reloading:
        print(f"reloading, seconds passed {round(time.time() - curent_time, 2)}", end="\r")
        if not is_reloading:
            break


def printUpload():
    curent_time = time.time()
    while True:
        print(f"uploading, seconds passed {round(time.time() - curent_time, 2)}", end="\r")
        if not is_uploading:
            print("------------------uploaded--------------------")
            break


is_uploading = False


def reload(param=1):
    global is_reloading
    if param == 1:
        uploadfile()
    is_reloading = True
    threading.Thread(target=print_time).start()
    response = requests.post(api_base_url + "/webapps/vincinemaapi.pythonanywhere.com/reload/",
                             headers={"Authorization": "Token " + api_token})
    is_reloading = False
    print(response.text)
    if response.status_code != 200:
        print("Error: webapp reload failed")
    else:
        print("------------------reloaded--------------------")


def uploadfile(file="D:\\VNTU\\1 course\\2 semestr\\web\\testflaks\\app.py"):
    filename = file.split('\\')[-1]
    with open(file, "rb") as f:
        file_data = f.read()
    global is_uploading
    is_uploading = True
    threading.Thread(target=printUpload).start()
    response = requests.post(api_base_url + f"/files/path/home/vincinemaApi/Cinema/{filename}",
                             headers={"Authorization": "Token " + api_token},
                             files={"content": (filename, file_data, "application/octet-stream")})
    is_uploading = False
    if response.status_code != 201 and response.status_code != 200:
        print("Error: Could not upload file.")
        exit()


def refilldb():
    global consindex
    GetConsoles(param=0)
    for console in consoles:
        if console["executable"] == "mysql":
            consindex = consoles.index(console)
            SendInput("drop table if exists sessions;\ndrop table if exists film;")
            print("SQL>>> drop table if exists sessions;")
            print("SQL>>> drop table if exists film;")
            break
    for console in consoles:
        if console["executable"] == "bash":
            consindex = consoles.index(console)
            SendInput("cd /home/vincinemaApi/Cinema\npython\nfrom app import db\ndb.create_all()\nexit()\npython newFilingFilms.py fill\necho 'Base refilled'")
            print("bash>>> cd /home/vincinemaApi/Cinema")
            print("bash>>> python")
            print("python>>> from app import db")
            print("python>>> db.create_all()")
            print("python>>> exit()")
            print("bash>>> python newFilingFilms.py")

            break


while True:
    GetOutput()
    command = input()
    if command == "reload":
        reload()
        input("press enter to continue")
    elif command == "exit":
        exit()
    elif command == "upload":
        uploadfile()
        input("press enter to continue")
    elif command == "upload -f":
        file = easygui.fileopenbox()
        uploadfile(file)
        input("press enter to continue")
    elif command == "reload -r":
        reload(0)
        input("press enter to continue")
    elif command == "url":
        os.system("start https://vincinemaapi.pythonanywhere.com/")
    elif command == "chconsole":
        GetConsoles()
    elif command == "refilldb":
        refilldb()
    elif command == "help":
        print('''
        reload - reloads webapp
        reload -r - reloads webapp without uploading
        url - opens webapp url
        upload - uploads app.py
        chconsole - changes console
        refilldb - refills database
        exit - exits
        ''')
        input("press enter to continue")
    else:
        SendInput(command)
