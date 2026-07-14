from pydantic import BaseModel, Field


class ValidateTime(BaseModel):
    second: int = Field(..., ge=0, le=60)
    minute: int = Field(..., ge=0, le=60)
    hour: int = Field(..., ge=0, le=60)


class TimeConverter:
    pass
