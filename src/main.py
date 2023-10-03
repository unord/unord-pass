import pyperclip
from selenium import webdriver
import selenium_tools
import studsys
import sys
import tools
import unord_sms


@tools.measure_time
def change_password_in_studsys(driver: webdriver, search_user: str) -> tuple[str, str]:
    # Change Password in Studsys and return the sms message
    studsys.find_user(driver, search_user)
    this_name = studsys.get_name(driver)
    this_user = studsys.get_username(driver)
    this_mobile = studsys.get_mobile_number(driver)
    print(f"Found user: {this_user}, ({this_name}), ({this_mobile})")
    print("**********************************************************************************\n")
    this_password = studsys.change_password(driver)
    sms_msg = studsys.create_msg(this_user, this_password)
    print("**********************************************************************************")
    print(f"* Message copied to clipboard and ready to be sent to mobile: ({this_mobile})  *")
    print("**********************************************************************************")
    return sms_msg, this_mobile


def main():
    while True:
        # Clear terminal
        tools.clear()

        # Start selenium webdriver headless
        driver = selenium_tools.get_webdriver()

        # Get username or cpr-number from user
        search_user = input("Enter username or cpr-number: ")

        # Change to password on student in Studsys
        sms_msg, this_mobile = change_password_in_studsys(driver, search_user)


        # Close selenium webdriver
        driver.close()

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

        # Print sms message
        print(sms_msg)

        # Copy sms message to clipboard
        pyperclip.copy(sms_msg)

        # Wait for user to press enter
        print(f"Response for sms.dk: {sms_response}")
        input("Press enter to to continue...")


if __name__ == '__main__':
    main()
