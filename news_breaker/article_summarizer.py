from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from news_breaker.browser import Browser
import json
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

DEVICE = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.53 Safari/537.36",
    "screen": {"width": 1920, "height": 1080},
    "viewport": {"width": 1280, "height": 720},
    "device_scale_factor": 1,
    "is_mobile": False,
    "has_touch": False,
    "default_browser_type": "chromium",
}


TEMPLATE = """
將以下文章總結成最多100字：

{article}
"""


class ArticleSummarizer:
    def __init__(self, url):
        self.url = url

    def get_prompt(self, article) -> list:
        chat_prompt = ChatPromptTemplate.from_messages(
            [HumanMessagePromptTemplate.from_template(TEMPLATE)]
        )

        return chat_prompt.format_prompt(article=article).to_messages()

    async def summarize(self) -> str:
        result = ""
        async with Browser() as browser:
            toolkit = PlayWrightBrowserToolkit.from_browser(
                async_browser=browser.get_browser()
            )
            tools = toolkit.get_tools()
            tools_by_name = {tool.name: tool for tool in tools}
            navigate_tool = tools_by_name["navigate_browser"]
            get_elements_tool = tools_by_name["get_elements"]
            print("step initialize")

            await navigate_tool.arun({"url": self.url})
            text = await get_elements_tool.arun({"selector": "article"})
            print("step get article")
            print(text)
            selected = json.loads(text)
            articles = map(lambda x: x["innerText"], selected)
            articles_str = "\n".join(articles)

            chat = ChatOpenAI(temperature=0)
            result = chat(self.get_prompt(articles_str)).content

        return result
