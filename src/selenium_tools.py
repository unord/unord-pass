from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager


def get_webdriver() -> webdriver:
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Set path to the chromedriver executable (automatically downloads the latest version)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver


def scroll_to_bottom(driver: webdriver) -> dict:

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

    return {'msg': 'Scrolled to bottom', 'success': True}


def get_chrome_driver_status(driver):
    try:
        driver.title
        return "Alive"
    except Exception:
        return "Dead"


def main():
    pass


if __name__ == '__main__':
    main()
