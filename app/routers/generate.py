from fastapi import APIRouter
from pydantic import BaseModel
from agents.plan import planning_agent   
from agents.research import create_search_topic
from agents.research import web_search_result
from agents.write import collect_topics

router = APIRouter()


class ResearchRequest(BaseModel):
    query: str

print(collect_topics)

@router.post("/query")
def research(request_formate: ResearchRequest):
    plan= planning_agent(request_formate.query)
    # websearch= create_search_topic(request_formate.query)
    websearch = [create_search_topic(task) for task in plan.tasks]
    search_result = [
        web_search_result(task, topic.search_topic)
        for task, topic in zip(plan.tasks, websearch)
    ]

    alltopic = collect_topics(websearch)
    print(alltopic)

    return {"plan": plan,
            "websearch": websearch,
            "search_result": search_result,
            "alltopic": alltopic
            }

# print(research.alltopic)
