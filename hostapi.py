import os

import requests

api_base_url = "https://www.pythonanywhere.com/api/v0/user/vincinemaApi"
api_token = '6085f0d381829a81ae376ffa70c250a422b2040a'

response = requests.get(api_base_url + "/consoles/", headers={"Authorization": "Token " + api_token})
bconsole = None
if response.status_code == 200:
    consoles = response.json()
    for console in consoles:
        if console["executable"] == "bash":
            bconsole = console
            break
    if bconsole is None:
        print("Error: Could not find bash console.")
        exit()
    else:
        print("Console found: " + bconsole["name"])
else:
    print("Error: Could not retrieve console data.")


def GetOutput():
    response = requests.get(api_base_url + "/consoles/{id}/get_latest_output/".format(id=bconsole["id"]),
                            headers={"Authorization": "Token " + api_token})
    if response.status_code == 200:
        print(f"{response.json()['output']}", end="")
    else:
        print("Error: Could not retrieve console output.")


def SendInput(text):
    print("waiting for response...")
    response = requests.post(api_base_url + "/consoles/{id}/send_input/".format(id=bconsole["id"]),
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
def reload():
    global is_reloading
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


while True:
    GetOutput()
    command = input()
    if command == "reload":
        reload()
    elif command == "exit":
        exit()
    else:
        SendInput(command)
        os.system("cls")
