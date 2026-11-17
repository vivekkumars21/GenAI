import os
from typing import TypedDict


class State(TypedDict):
    topic: str
    summmary: str
    score: int


# second type of state building for agentic workflow

from pydantic import BaseModel, field_validator


class State(BaseModel):
    topic: str
    score: int
    summary: str = ""

    @field_validator
    def score_positive(cls, v):
        if v < 0:
            raise ValueError("score must be positive")


# 3d way to build agentic workflow using py dataclasses

from dataclasses import dataclass, field


@dataclass
class State:
    topic: str
    summary: str = ""
    message: list = field(default_factory=list)


# 4th way is just use defult langgraph

from langgraph.graph import MessagesState


class State(MessagesState):
    user_name: str
    language: str
