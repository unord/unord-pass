from decouple import config
import json
import pyperclip
import requests
import sys


# Global variables
try:
    SMS_API_KEY = config('SMS_API_KEY')
except Exception as e:
    print("Error: Could not find SMS_API_KEY in '.env' in project root")
    print("Please create '.env' in project root and add STUDSYS_USERNAME, STUDSYS_PASSWORD, and SMS_API_KEY")
    print(f"Exception: {e}")
    print("Enter STUDSYS_USERNAME and STUDSYS_PASSWORD to clipboard or exit by pressing 'CTRL + C'")
    input_username = input("Please enter your STUDSYS_USERNAME: ")
    input_password = input("Please enter your STUDSYS_PASSWORD: ")
    send_to_clipboard = f"STUDSYS_USERNAME={input_username}\nSTUDSYS_PASSWORD={input_password}\nSMS_API_KEY="
    pyperclip.copy(send_to_clipboard)
    print("Exiting...")
    sys.exit()


def send_sms(this_cellphone: str, this_msg: str) -> requests.Response:
    url = "https://api.sms.dk/v1/sms/send"
    payload = json.dumps({
        "receiver": int("45" + str(this_cellphone)),
        "senderName": "U/NORD",
        "message": this_msg,
        "format": "gsm",
        "encoding": "utf8",
      })

    headers = {
     'Authorization': 'Bearer ' + config('SMS_API_KEY'),
     'Content-Type': 'application/json'
     }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def main():
    pass


if __name__ == '__main__':
    main()
