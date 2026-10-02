from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from typing import List
from prompt.plan_prompt import mpt


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY
)

class ResearchTask(BaseModel):
    task_id: int
    title: str
    description: str


class Planning(BaseModel):
    topic: str
    tasks: List[ResearchTask] = Field(min_length=7, max_length=9)


planner = llm.with_structured_output(Planning)


def planning_agent(topic: str) -> Planning:
    result = planner.invoke(mpt(topic))

    return result