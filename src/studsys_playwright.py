import sys
import time
import traceback
from playwright.sync_api import sync_playwright


class StudsysBot:
    def __init__(self, studsys_user, studsys_password, browser_headless=True):
        self.studsys_user = studsys_user
        self.studsys_password = studsys_password
        self.browser_headless = browser_headless
        self.playwright = None
        self.browser = None
        self.page = None


    def start_playwright(self):
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.browser_headless)
            self.page = self.browser.new_page()
        except Exception as e:
            print(f"Error starting Playwright: {e}")
            print(traceback.format_exc())
            sys.exit(1)

    def stop_playwright(self):
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"Error stopping Playwright: {e}")
            print(traceback.format_exc())

    def login(self) -> dict:
        try:
            # Go to Studsys main page to login
            self.page.goto(f"https://{self.studsys_user}:{self.studsys_password}@studsys2020.efif.dk/")
            print(f"https://{self.studsys_user}:{self.studsys_password}@studsys2021.efif.dk/")
            # Check if the specific element exists to verify login success
            welcome_message = self.page.wait_for_selector("h2.no_title", timeout=5000)  # Timeout set to 5 seconds
            if welcome_message and "Velkommen til StudSys" in welcome_message.inner_text():
                return {"status": "success", "message": "Login successful"}
            else:
                return {"status": "failure", "message": "Login failed"}
        except Exception as e:
            # Handle any exceptions that occur during login
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    class Student:
        def __init__(self, page, student_username):
            self.page = page
            self.student_username = student_username

        def find_student(self) -> dict:
            try:
                # find user in Studsys
                self.page.goto(f"https://studsys2020.efif.dk/Account/Search.aspx?Query={self.student_username}")

                # Select first user
                studsys_user = self.page.locator("a:has-text('1')")
                assert studsys_user.count() > 0, "Element with text '1' not found"

                studsys_user.click()

                # Return success
                return {'msg': 'Found user', 'success': True}
            except Exception as e:
                print(f"Error finding user: {e}")
                print(traceback.format_exc())
                # take screenshot
                self.page.screenshot(path=f"error_{time.time()}.png")
                return {'msg': 'Error finding user', 'success': False}

        def get_name(self) -> dict:
            try:
                # Retrive name from Studsys
                name = self.page.inner_text("#firstnameLabel") + " " + self.page.inner_text("#lastnameLabel")
                return {'msg': name, 'success': True}
            except Exception as e:
                print(f"Error getting name: {e}")
                print(traceback.format_exc())
                return {'msg': 'Error getting name', 'success': False}

        def get_username(self) -> dict:
            try:
                # Retrive username from Studsys
                username = self.page.inner_text("#usernameLabel")
                return {'msg': username, 'success': True}
            except Exception as e:
                print(f"Error getting username: {e}")
                print(traceback.format_exc())
                return {'msg': 'Error getting username', 'success': False}

        def get_mobile_number(self) -> str:
            try:
                # Retrive mobile number from Studsys
                user_mobile = self.page.inner_text("#cellPhoneNoLabel")
                return {'msg': user_mobile, 'success': True}
            except Exception as e:
                print(f"Error getting mobile number: {e}")
                print(traceback.format_exc())
                return {'msg': 'Error getting mobile number', 'success': False}

        def get_password(self) -> dict:
            try:
                # Retrive password from Studsys
                self.page.hover("#initialPasswordLabel")
                password = self.page.inner_text("#initialPasswordLabel")
                return {'msg': password, 'success': True}
            except Exception as e:
                print(f"Error getting password: {e}")
                print(traceback.format_exc())
                return {'msg': 'Error getting password', 'success': False}



def main():
    test_bot = StudsysBot("gore", "ChallengerOV-099")
    test_bot.start_playwright()
    login_result = test_bot.login()
    if login_result['status'] == 'success':
        test_bot.student = test_bot.Student(test_bot.page, "unordetta")
        find_student_result = test_bot.student.find_student()
        if find_student_result['success']:
            get_name_result = test_bot.student.get_name()
            if get_name_result['success']:
                get_username_result = test_bot.student.get_username()
                if get_username_result['success']:
                    get_mobile_number_result = test_bot.student.get_mobile_number()
                    if get_mobile_number_result['success']:
                        get_password_result = test_bot.student.get_password()
                        if get_password_result['success']:
                            print(f"Name: {get_name_result['msg']}")
                            print(f"Username: {get_username_result['msg']}")
                            print(f"Mobile number: {get_mobile_number_result['msg']}")
                            print(f"Password: {get_password_result['msg']}")
                        else:
                            print(get_password_result['msg'])
                    else:
                        print(get_mobile_number_result['msg'])
                else:
                    print(get_username_result['msg'])
            else:
                print(get_name_result['msg'])
        else:
            print(find_student_result['msg'])


if __name__ == '__main__':
    main()
