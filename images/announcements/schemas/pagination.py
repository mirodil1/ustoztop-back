from typing import Generic, List, Optional, TypeVar

from pydantic import AnyHttpUrl, Field
from pydantic.generics import GenericModel

M = TypeVar("M")

class PaginatedPerPageResponse(GenericModel, Generic[M]):
    count: int = Field(description="Number of total items")
    next_page: AnyHttpUrl | None = Field(
        None,
        description="url of the next page if it exists",
    )
    previous_page: AnyHttpUrl | None = Field(
        None,
        description="url of the previous page if it exists",
    )
    items: list[M] = Field(description="List of items returned in a paginated response")
