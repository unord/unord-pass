# studsys.py

from decouple import config
import pyperclip
import sys
from playwright.sync_api import Page, TimeoutError
from colorama import Fore, Style  # Add this import

def change_password(page: Page) -> str:
    # Click the "Reset Password" button
    page.click("#showResetPasswordDialogButton")

    # If "resetLectioPasswordCheckBox" is not checked, then check it
    checkbox_reset_password_lectio = page.query_selector("#resetLectioPasswordCheckBox")
    if not checkbox_reset_password_lectio.is_checked():
        checkbox_reset_password_lectio.click()

    # If "mustChangePasswordAtNextLogonCheckBox" is checked, then uncheck it
    checkbox_change_password_next_login = page.query_selector("#mustChangePasswordAtNextLogonCheckBox")
    if checkbox_change_password_next_login.is_checked():
        checkbox_change_password_next_login.click()

    # Click the "resetPasswordButton"
    page.click("#resetPasswordButton")

    # Get new password from "initialPasswordLabel"
    i = 0
    studsys_password = ""
    while "••••••••••••" in studsys_password or studsys_password == "":
        i += 1
        if i == 20:
            print("Error: Could not find new password")
            sys.exit()
        element_hover_password = page.wait_for_selector("#initialPasswordLabel")
        element_hover_password.hover()
        studsys_password = element_hover_password.text_content()

    return studsys_password

def create_msg(this_user: str, this_password: str) -> tuple[str, str]:
    # Plain message for SMS
    plain_msg = (
        f"Du kan bruge de her oplysninger til Lectio, Office.com, Teams, fjernskrivebord(u-term.efif.dk) og logge på skolens WIFI(UNORD WIFI)\n\n"
        f"Brugernavn er: {this_user}\n"
        f"Adgangskode er: {this_password}\n"
        f"Din skole email er: {this_user}@unord.dk\n\n"
        f"Du kan skifte din adgangskode på https://mobil.efif.dk\n"
        f"Hvis din konto har været låst går der 30 min før den bliver låst op.\n"
    )
    # Colored message for terminal output
    colored_msg = (
        f"Du kan bruge de her oplysninger til Lectio, Office.com, Teams, fjernskrivebord(u-term.efif.dk) og logge på skolens WIFI(UNORD WIFI)\n\n"
        f"Brugernavn er: {Fore.CYAN}{this_user}{Style.RESET_ALL}\n"
        f"Adgangskode er: {Fore.CYAN}{this_password}{Style.RESET_ALL}\n"
        f"Din skole email er: {Fore.CYAN}{this_user}@unord.dk{Style.RESET_ALL}\n\n"
        f"Du kan skifte din adgangskode på https://mobil.efif.dk\n"
        f"Hvis din konto har været låst går der 30 min før den bliver låst op.\n"
    )
    return plain_msg, colored_msg

def find_user(page: Page, this_user: str) -> None:
    # Construct the URL without basic authentication
    studsys_url = f"https://studsys2020.efif.dk/Account/Search.aspx?Query={this_user}"
    page.goto(studsys_url)
    try:
        # Wait for the link text '1' to be available and click it
        page.wait_for_selector("text='1'", timeout=5000)
        page.click("text='1'")
    except TimeoutError:
        print("Error: User not found.")
        sys.exit()

def get_mobile_number(page: Page) -> str:
    # Retrieve mobile number from Studsys
    try:
        user_mobile_element = page.wait_for_selector("#cellPhoneNoLabel", timeout=5000)
        user_mobile = user_mobile_element.text_content()
        return user_mobile
    except TimeoutError:
        user_mobile = "Could not find mobile number"
        return user_mobile

def get_name(page: Page) -> str:
    # Retrieve name from Studsys
    try:
        firstname_element = page.wait_for_selector("#firstnameLabel", timeout=5000)
        firstname = firstname_element.text_content()
        lastname_element = page.wait_for_selector("#lastnameLabel", timeout=5000)
        lastname = lastname_element.text_content()
        name = firstname + " " + lastname
        return name
    except TimeoutError:
        print("Error: Could not find name elements on the page.")
        sys.exit()

def get_username(page: Page) -> str:
    # Retrieve username from Studsys
    try:
        username_element = page.wait_for_selector("#usernameLabel", timeout=5000)
        user = username_element.text_content()
        return user
    except TimeoutError:
        print("Error: Could not find username element on the page.")
        sys.exit()

def main():
    pass

if __name__ == '__main__':
    main()
