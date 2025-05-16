from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(default=6, ge=0, le=100, description="Number of elements on a page")
    offset: int = Field(default=0, ge=0, description="offset for pagination")

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]