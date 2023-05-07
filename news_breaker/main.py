import asyncio
import sys
from news_breaker.article_summarizer_v2 import ArticleSummarizer
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback


async def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage: python main.py <url>")
        return -1

    url = args[0]
    summarizer = ArticleSummarizer(url)

    with get_openai_callback() as cb:
        result = await summarizer.summarize()
        print(f"Result: {result}")
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
