from typing import List, Dict, Any

from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


class IceBreaker(BaseModel):
    ice_breakers: List[str] = Field(description="ice breaker list")

    def to_dict(self) -> Dict[str, Any]:
        return {"ice_breakers": self.ice_breakers}


class TopicOfInterest(BaseModel):
    topics_of_interest: List[str] = Field(
        description="topic that might interest the person"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {"topics_of_interest": self.topics_of_interest}
