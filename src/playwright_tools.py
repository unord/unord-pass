# playwright_tools.py

from playwright.sync_api import sync_playwright

class PlaywrightTools:
    def __init__(self, username, password):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context(http_credentials={"username": username, "password": password})
        self.page = self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def get_page(self):
        return self.page

    def scroll_to_bottom(self):
        page = self.page
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        return {'msg': 'Scrolled to bottom', 'success': True}

    def get_driver_status(self):
        try:
            self.page.title()
            return "Alive"
        except Exception:
            return "Dead"

def main():
    pass

if __name__ == '__main__':
    main()
