from fastapi import APIRouter
from pydantic import BaseModel
from agents.plan import planning_agent   
from agents.research import create_search_topic
from agents.research import web_search_result
from agents.write import write_result, Write_Input
from concurrent.futures import ThreadPoolExecutor


router = APIRouter()


class ResearchRequest(BaseModel):
    query: str

# print(collect_topics)

@router.post("/query")
def research(request_formate: ResearchRequest):
    # plan= planning_agent(request_formate.query)
    with ThreadPoolExecutor(max_workers=3) as executor:
        plan= planning_agent(request_formate.query)
        # websearch= create_search_topic(request_formate.query)

        # ✅ Sab search topics parallel mein banenge
        websearch = list(executor.map(create_search_topic, plan.tasks))

        # ✅ Sab web searches parallel mein honge
        search_result = list(
            executor.map(
                lambda pair: web_search_result(pair[0], pair[1].search_topic),
                zip(plan.tasks, websearch),
            )
        )

        all_topics = [topic.search_topic for topic in websearch]

        # ✅ Har research result ke liye write_result parallel mein call hoga
        write = list(
            executor.map(
                lambda result: write_result(
                    Write_Input(
                        input=result.model_dump(),
                        all_topics=all_topics,
                    )
                ),
                search_result,
            )
        )

    return {"plan": plan,
            "websearch": websearch,
            "search_result": search_result,
            "write": write
                        }

# print(research.alltopic)
