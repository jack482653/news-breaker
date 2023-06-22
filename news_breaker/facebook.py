import re

from news_breaker.article_summarizer import ArticleSummarizer
from news_breaker.models.loggable import Loggable
from news_breaker.utils.browser import Browser

CONFIGS = {
    "ETtoday": {
        "page": "ETtoday",
        "link_regex": "ettoday\.net\/news",
    }
}

TAGS = ["#by_news_breaker", "#台灣新聞淨化運動"]


class Facebook(metaclass=Loggable):
    def __init__(self, username, password, name, open_browser=False):
        self.username = username
        self.password = password
        if not CONFIGS[name]:
            raise ValueError(f"Invalid name: {name}")
        self.config = CONFIGS[name]
        self.browser = Browser(headless=not open_browser)
        self.is_login = False

    async def run(self):
        async with self.browser:
            await self.login()
            post_page = await self.goto_latest_post_page()

            url = await self.get_one_news_links(post_page)
            if not url:
                self.__logger.info("No new news")
                return

            self.__logger.info(f"Got news: {url}")
            summarizer = ArticleSummarizer(url)
            text = await summarizer.summarize()
            await self.comment(post_page, text)

    async def login(self):
        self.__logger.info("Logging in...")
        page = await self.browser.get_or_open_page()
        # Navigate to Facebook login page
        await page.goto("https://www.facebook.com/login")

        # Fill in login form and submit
        await page.fill("#email", self.username)
        await page.fill("#pass", self.password)
        await page.click("#loginbutton")

        # Wait for login to complete
        await page.wait_for_selector("[aria-label='Messenger']")
        self.__logger.info("Login complete")
        self.is_login = True

    async def goto_latest_post_page(self):
        page = await self.browser.get_or_open_page()
        await page.goto(f"https://www.facebook.com/{self.config['page']}")
        post_link = (
            page.get_by_role("link")
            .get_by_text(re.compile("(\dm|\d分鐘|just now|剛剛)", re.IGNORECASE))
            .locator("nth=0")
        )
        post_link = await post_link.click()

        return page

    async def get_one_news_links(self, page):
        try:
            return (
                await page.get_by_text(
                    re.compile(self.config["link_regex"], re.IGNORECASE)
                )
                .locator("nth=0")
                .inner_text()
            )
        except Exception as e:
            self.__logger.error(f"Failed to get news link: {e}")
            return None

    async def comment(self, post_detail, text):
        # merge text and tags
        text_and_tags = text + "\n\n" + "\n".join(TAGS)
        comment = post_detail.get_by_role("textbox").locator("nth=0")

        await post_detail.pause()
        await comment.fill(text_and_tags)
        await comment.press("Enter")
