from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(
        default=6, ge=0, le=100, description="Number of elements on a page"
    )
    page: int = Field(default=1, ge=1, description="Page for pagination")


PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]
