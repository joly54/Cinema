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
        print(response.json()["output"], end="")
    else:
        print("Error: Could not retrieve console output.")
def SendInput(text):
    print("waiting for response...")
    response = requests.post(api_base_url + "/consoles/{id}/send_input/".format(id=bconsole["id"]),
                             data={"input": text + "\n"}, headers={"Authorization": "Token " + api_token})
    print(response.text)
    if response.status_code != 200:
        print("Error: Could not send input to console.")
while True:
    GetOutput()
    SendInput(input())
    os.system("cls")


