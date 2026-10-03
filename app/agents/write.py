from pydantic import BaseModel, Field
from typing import List
from agents.research import create_search_topic
from agents.research import ResearchTopicName
from config import GROQ_API_KEY
from langchain_groq import ChatGroq
from agents.research import web_search_result

class ResearchResult(BaseModel):
    task_id: int
    title: str
    output: str
    sources: List[str] = []

class AllTopic(BaseModel):
    all_topics: List[str] = []

class Write_Input(BaseModel):
    input: ResearchResult
    # all_topics: AllTopic
    all_topics: List[str]

class Write_Output(BaseModel):
    heading: str
    body: str
    links: str


def collect_topics(topics: List[create_search_topic]) -> AllTopic:
    topic_list = [t.search_topic for t in topics]
    result = AllTopic(all_topics=topic_list)

    # print(result, "dfghjk")   # terminal mein dikhega
    return result   # swagger mein dikhega



llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=GROQ_API_KEY
)

def write_result(data: Write_Input) -> Write_Output:

    structured_llm = llm.with_structured_output(Write_Output)

    prompt = f"""
You are a research report writer.

You will receive:

1. Research result of the current topic.
2. List of all research topics.

Your task is to read the research carefully and create a clear
research section.

Current Research Title:
{data.input.title}

Current Research:
{data.input.output}

Sources:
{data.input.sources}

All Research Topics:
{data.all_topics}

Create the output in this format:

heading:
A suitable heading for this research section.

body:
Write a clear and informative explanation based only on the
provided research.

links:
Return the useful source links from the provided sources.

Do not invent information or sources.
"""

    response = structured_llm.invoke(prompt)

    return response