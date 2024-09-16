# main.py

import pyperclip
import sys
import tools
import unord_sms
from decouple import config
import playwright_tools
import studsys

from colorama import init  # Add this import
init(autoreset=True)       # Initialize colorama

STUDSYS_USERNAME = config('STUDSYS_USERNAME')
STUDSYS_PASSWORD = config('STUDSYS_PASSWORD')

@tools.measure_time
def change_password_in_studsys(page, search_user: str) -> tuple[str, str, str]:
    # Change Password in Studsys and return the sms message
    studsys.find_user(page, search_user)
    this_name = studsys.get_name(page)
    this_user = studsys.get_username(page)
    this_mobile = studsys.get_mobile_number(page)
    print(f"Found user: {this_user}, ({this_name}), ({this_mobile})")
    print("**********************************************************************************\n")
    this_password = studsys.change_password(page)
    sms_msg, colored_msg = studsys.create_msg(this_user, this_password)
    print("**********************************************************************************")
    print(f"* Message copied to clipboard and ready to be sent to mobile: ({this_mobile})  *")
    print("**********************************************************************************")
    return sms_msg, colored_msg, this_mobile

def playwright_setup() -> None:
    while True:
        # Clear terminal
        tools.clear()

        # Start Playwright with HTTP credentials
        p_tools = playwright_tools.PlaywrightTools(STUDSYS_USERNAME, STUDSYS_PASSWORD)
        page = p_tools.get_page()

        # Get username or cpr-number from user
        search_user = input("Enter username or cpr-number: ")

        # Change password on student in Studsys
        sms_msg, colored_msg, this_mobile = change_password_in_studsys(page, search_user)

        # Close Playwright
        p_tools.close()

        # Send sms to user
        sms_response = {}
        print(f"Is this the correct mobile number: {this_mobile}")
        send_sms = input("Send sms to user? (y/n): ")
        if send_sms == "y":
            this_mobile = this_mobile.replace(" ", "").replace("+45", "")
            sms_response = unord_sms.send_sms(this_mobile, sms_msg)
        else:
            this_mobile = input("Enter new mobile number: ")
            sms_response = unord_sms.send_sms(this_mobile, sms_msg)
        print(f"SMS sent to {this_mobile}")

        # Print colored sms message to terminal
        print(colored_msg)

        # Copy plain sms message to clipboard
        pyperclip.copy(sms_msg)

        # Wait for user to press enter
        print(f"Response for sms.dk: {sms_response}")
        input("Press enter to continue...")

def main():
    playwright_setup()

if __name__ == '__main__':
    main()
