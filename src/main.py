# main.py

import pyperclip
import sys
import tools
import unord_sms
from decouple import config
import playwright_tools
import studsys

from colorama import init  # Add this import

init(autoreset=True)  # Initialize colorama

# Configuration Variables
STUDSYS_USERNAME = config('STUDSYS_USERNAME')
STUDSYS_PASSWORD = config('STUDSYS_PASSWORD')


@tools.measure_time
def change_password_in_studsys(page, search_user: str) -> tuple[str, str, str]:
    """
    Change the password for a user in Studsys and prepare the SMS message.

    Args:
        page: Playwright page object.
        search_user (str): Username or CPR number to search.

    Returns:
        tuple: Contains the SMS message, colored message, and mobile number.
    """
    # Find and retrieve user details
    studsys.find_user(page, search_user)
    this_name = studsys.get_name(page)
    this_user = studsys.get_username(page)
    this_mobile = studsys.get_mobile_number(page)

    print(f"Found user: {this_user}, ({this_name}), ({this_mobile})")
    print("**********************************************************************************\n")

    # Change password and create messages
    this_password = studsys.change_password(page)
    sms_msg, colored_msg = studsys.create_msg(this_user, this_password)

    print("**********************************************************************************")
    print(f"* Message copied to clipboard and ready to be sent to mobile: ({this_mobile})  *")
    print("**********************************************************************************")

    return sms_msg, colored_msg, this_mobile


def initialize_playwright():
    """
    Initialize Playwright and return the PlaywrightTools and page instances.

    Returns:
        tuple: PlaywrightTools instance and Playwright page object.
    """
    p_tools = playwright_tools.PlaywrightTools(STUDSYS_USERNAME, STUDSYS_PASSWORD)
    page = p_tools.get_page()
    return p_tools, page


def send_sms_to_user(this_mobile: str, sms_msg: str) -> dict:
    """
    Send SMS to the user.

    Args:
        this_mobile (str): Mobile number of the user.
        sms_msg (str): SMS message content.

    Returns:
        dict: Response from the SMS service.
    """
    sms_response = {}
    print(f"Is this the correct mobile number: {this_mobile}")
    send_sms = input("Send sms to user? (y/n): ").strip().lower()

    if send_sms == "y":
        # Normalize mobile number by removing spaces and country code
        this_mobile = this_mobile.replace(" ", "").replace("+45", "")
    else:
        # Prompt for a new mobile number
        this_mobile = input("Enter new mobile number: ").strip()
        this_mobile = this_mobile.replace(" ", "").replace("+45", "")

    sms_response = unord_sms.send_sms(this_mobile, sms_msg)
    print(f"SMS sent to {this_mobile}")
    return sms_response, this_mobile


def prompt_continue_or_quit() -> bool:
    """
    Prompt the user to continue or quit the program.

    Returns:
        bool: True if the user wants to continue, False if the user wants to quit.
    """
    user_input = input('Press enter to continue or "q" to quit...').strip().lower()
    if user_input == "q":
        return False
    return True


def process_password_change(page):
    """
    Process a single password change operation.

    Args:
        page: Playwright page object.
    """
    # Clear terminal
    tools.clear()

    # Get username or CPR number from user
    search_user = input("Enter username or CPR-number: ").strip()
    if not search_user:
        print("Invalid input. Please enter a valid username or CPR number.")
        return

    # Change password in Studsys
    sms_msg, colored_msg, this_mobile = change_password_in_studsys(page, search_user)

    # Send SMS to user
    sms_response, this_mobile = send_sms_to_user(this_mobile, sms_msg)

    # Print colored SMS message to terminal
    print(colored_msg)

    # Copy plain SMS message to clipboard
    pyperclip.copy(sms_msg)

    # Print SMS service response
    print(f"Response from SMS service: {sms_response}")


def main():
    """
    Main function to orchestrate the password change and SMS sending process.
    """
    # Initialize Playwright once
    p_tools, page = initialize_playwright()

    try:
        while True:
            process_password_change(page)

            # Prompt user to continue or quit
            if not prompt_continue_or_quit():
                print("Exiting the program. Goodbye!")
                break  # Exit the loop gracefully

            # Optional UI enhancement
            print("\n" + "=" * 80 + "\n")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure Playwright closes even if an error occurs
        p_tools.close()


if __name__ == '__main__':
    main()
