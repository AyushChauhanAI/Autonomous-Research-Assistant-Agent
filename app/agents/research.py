from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from config import TAVILY_API_KEY
from tavily import TavilyClient
from prompt.search_prompt import websearch


class ResearchTask(BaseModel):
    task_id: int
    title: str
    description: str


class ResearchTopicName(BaseModel):
    search_topic: str

class ResearchResult(BaseModel):
    task_id: int
    title: str
    output: str
    sources: List[str] = []



llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=GROQ_API_KEY
)


research_topic_llm=llm.with_structured_output(ResearchTopicName)


def create_search_topic(task: ResearchTask) ->ResearchTopicName:
    result=research_topic_llm.invoke(websearch(task))
    # print(result)

    return result


tavily = TavilyClient(api_key=TAVILY_API_KEY)
def web_search_result(task: ResearchTask, topic: str) -> ResearchResult:

    response = tavily.search(
        query=topic,
        max_results=5
    )

    output = "\n\n".join(
        result["content"]
        for result in response["results"]
    )

    sources = [
        result["url"]
        for result in response["results"]
    ]

    return ResearchResult(
        task_id=task.task_id,
        title=task.title,
        output=output,
        sources=sources
    )