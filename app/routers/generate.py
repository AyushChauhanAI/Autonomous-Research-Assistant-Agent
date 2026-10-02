from fastapi import APIRouter
from pydantic import BaseModel
from agents.plan import planning_agent   

router = APIRouter()


class ResearchRequest(BaseModel):
    query: str


@router.post("/query")
def research(request_formate: ResearchRequest):
    plan= planning_agent(request_formate.query)

    return plan