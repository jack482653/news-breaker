import json

from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from news_breaker.utils.browser import Browser

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
