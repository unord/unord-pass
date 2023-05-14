from decouple import config
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import sys


# Global variables
try:
    STUDSYS_USERNAME = config('STUDSYS_USERNAME')
    STUDSYS_PASSWORD = config('STUDSYS_PASSWORD')
except Exception as e:
    print("Error: Could not find STUDSYS_USERNAME and/or STUDSYS_PASSWORD in '.env' in project root")
    print("Please create '.env' in project root and add STUDSYS_USERNAME,  STUDSYS_PASSWORD, and SMS_API_KEY")
    print(f"Exception: {e}")
    print("Enter STUDSYS_USERNAME and STUDSYS_PASSWORD to clipboard or exit by pressing 'CTRL + C'")
    input_username = input("Please enter your STUDSYS_USERNAME: ")
    input_password = input("Please enter your STUDSYS_PASSWORD: ")
    send_to_clipboard = f"STUDSYS_USERNAME={input_username}\nSTUDSYS_PASSWORD={input_password}\nSMS_API_KEY="
    pyperclip.copy(send_to_clipboard)
    print("Exiting...")
    sys.exit()


def change_password(driver: webdriver) -> str:
    # Pushing the "Reset Password" button
    button_rest_password = driver.find_element(By.ID, "showResetPasswordDialogButton")
    button_rest_password.click()

    # If "resetLectioPasswordCheckBox" is not checked, then check it
    checkbox_reset_password_lectio = driver.find_element(By.ID, "resetLectioPasswordCheckBox")
    if not checkbox_reset_password_lectio.get_attribute('checked'):
        checkbox_reset_password_lectio = driver.find_element_by(By.XPATH, ".//*[contains(text(),'Reset Lectio password')]")
        checkbox_reset_password_lectio.click()

    # If "mustChangePasswordAtNextLogonCheckBox" is not checked, then check it
    checkbox_change_password_next_login = driver.find_element(By.ID, "mustChangePasswordAtNextLogonCheckBox")
    if checkbox_change_password_next_login.get_attribute('checked'):
        checkbox_change_password_next_login.click()

    # If "reset_password_commit" is not checked, then check it
    reset_password_commit = driver.find_element(By.ID, "resetPasswordButton")
    reset_password_commit.click()

    # Get new password from "initialPasswordLabel"
    element_hover_password = driver.find_element(By.ID, "initialPasswordLabel")
    hover_password = ActionChains(driver).move_to_element(element_hover_password)
    hover_password.perform()
    studsys_password = format(driver.find_element(By.ID, "initialPasswordLabel").text)

    i = 0
    while "••••••••••••" in studsys_password:
        i += 1
        if i == 20:
            print("Error: Could not find new password")
            sys.exit()
        element_hover_password = driver.find_element(By.ID, "initialPasswordLabel")
        hover_password = ActionChains(driver).move_to_element(element_hover_password)
        hover_password.perform()
        studsys_password = format(driver.find_element(By.ID, "initialPasswordLabel").text)

    return studsys_password


def create_msg(this_user: str, this_password: str) -> str:
    copy_paste_msg = f"Du kan bruge de her oplysninger ti Lectio, Office.com, Teams, fjernskrivebord(u-term.efif.dk) og logge på skolens WIFI(UNORD WIFI)\n\n"
    copy_paste_msg = copy_paste_msg + f"Brugernavn er: {this_user}\n"
    copy_paste_msg = copy_paste_msg + f"Adgangskode er: {this_password}\n"
    copy_paste_msg = copy_paste_msg + f"Din skole email er: {this_user}@unord.dk\n\n"
    copy_paste_msg = copy_paste_msg + f"Du kan skifte din adgangskode på https://mobil.efif.dk\n"
    copy_paste_msg = copy_paste_msg + f"Hvis din konto har været låst går der 30 min før den bliver låst op.\n"
    return copy_paste_msg


def find_user(driver: webdriver, this_user: str) -> None:
    # Find user in Studsys
    driver.get(f"https://{STUDSYS_USERNAME}:{STUDSYS_PASSWORD}@studsys2020.efif.dk/Account/Search.aspx?Query={this_user}")

    i = 0
    while i < 100:
        try:
            studsys_user = driver.find_element(By.LINK_TEXT, "1")
            studsys_user.click()
            i = 100
        except NoSuchElementException:
            if i == 99:
                print(f"Error: {e}")
                print(f"Exiting...")
                sys.exit()


def get_mobile_number(driver: webdriver) -> str:
    # Retrive mobile number from Studsys
    i = 0
    while i < 20:
        try:
            user_mobile = driver.find_element(By.ID, "cellPhoneNoLabel").text
            i = 20
            return user_mobile
        except NoSuchElementException:
            if i == 19:
                user_mobile = "Could not find mobile number"
                return user_mobile



def get_name(driver: webdriver) -> str:
    # Retrive name from Studsys
    name = driver.find_element(By.ID, "firstnameLabel").text + " " + driver.find_element(By.ID, "lastnameLabel").text
    return name


def get_username(driver: webdriver) -> str:
    # Retrive username from Studsys
    user = driver.find_element(By.ID, "usernameLabel").text
    return user


def main():
    pass


if __name__ == '__main__':
    main()
