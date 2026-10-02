from pydantic import BaseModel, Field
from typing import List
from agents.research import create_search_topic
from agents.research import ResearchTopicName

class AllTopic(BaseModel):
    all_topics: List[str] = []

class Write_Input(BaseModel):
    input: ResearchResult
    all_topics: AllTopic

class Write_Output(BaseModel):
    heading: str
    body: str
    links: str


def collect_topics(topics: List[create_search_topic]) -> AllTopic:
    topic_list = [t.search_topic for t in topics]
    result = AllTopic(all_topics=topic_list)

    print(result, "dfghjk")   # terminal mein dikhega
    return result   # swagger mein dikhega