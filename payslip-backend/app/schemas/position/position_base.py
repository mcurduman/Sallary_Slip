from pydantic import BaseModel, Field   
class PositionBase(BaseModel):
    title: str = Field(..., alias="title")
