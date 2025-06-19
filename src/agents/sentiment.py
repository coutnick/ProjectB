import logging
from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


class SentimentAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key, temperature=0)
        self.prompt = PromptTemplate(
            input_variables=['text'],
            template="""You are a crypto sentiment classifier. \
Given the following news text, classify overall sentiment as bullish, bearish or neutral.\n{text}\nSentiment:""",
        )

    async def analyze(self, texts: List[str]) -> str:
        joined = '\n'.join(texts)
        msg = self.prompt.format(text=joined)
        resp = await self.llm.apredict(msg)
        return resp.strip().lower()
