from playwright.async_api import async_playwright

DEVICE = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.53 Safari/537.36",
    "screen": {"width": 1920, "height": 1080},
    "viewport": {"width": 1280, "height": 720},
    "device_scale_factor": 1,
    "is_mobile": False,
    "has_touch": False,
    "default_browser_type": "chromium",
}


class Browser:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None

    async def init(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        await self.browser.new_context(**DEVICE)

    def get_browser(self):
        return self.browser

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
