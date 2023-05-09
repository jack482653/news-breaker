from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from news_breaker.browser import Browser
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models.openai import ChatOpenAI
from langchain import PromptTemplate
from news_breaker.get_elements import GetElementsToolUtf8

TEMPLATE = """
1. 根據連結使用 selector: article || .fncnews-content, attributes: [innerText] 取得 innerText
2. 以台灣慣用詞彙產生100字以內的繁體中文總結。

連結：{url}
"""


class ArticleSummarizer:
    def __init__(self, url):
        self.url = url

    def get_prompt(self) -> str:
        prompt = PromptTemplate(
            input_variables=["url"],
            template=TEMPLATE,
        )

        return prompt.format(url=self.url)

    async def summarize(self) -> str:
        result = ""
        async with Browser() as browser:
            # Initialize playwright toolkit
            toolkit = PlayWrightBrowserToolkit.from_browser(
                async_browser=browser.get_browser()
            )
            tools = toolkit.get_tools()
            tools_by_name = {tool.name: tool for tool in tools}
            navigate_tool = tools_by_name["navigate_browser"]
            # we use GetElementsToolUtf8 instead of GetElementsTool
            # because we want to get utf8 text instead of ascii text
            get_elements_tool = GetElementsToolUtf8.from_browser(
                async_browser=browser.get_browser()
            )
            # Initialize agent and model
            chat = ChatOpenAI(temperature=0)
            agent_chain = initialize_agent(
                [navigate_tool, get_elements_tool],
                chat,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
            )
            # Run agent
            result = await agent_chain.arun(self.get_prompt())

        return result