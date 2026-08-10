from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy.sql import Select

class PaginationParams:
    """Dependency for Getting pagination parameters from Query Parameters
    """
    def __init__(
        self,
        page: int = Query(1, ge=1, description="page number should be grather or equal than 1"),
        size: int = Query(10, ge=1, le=100, description="Maximum items per page can be 100 item")
    ):
        self.page = page
        self.size = size

    @property
    def offset(self) -> int:
        """Calculates offset for database query

        Returns:
            offset (int): database offset
        """
        return (self.page - 1) * self.size

def apply_pagination(statement: Select, pagination: PaginationParams) -> Select:
    """Helper function for implementing Limit and Offset on SQLAlchemy database Query

    Returns:
        _type_: _description_
    """
    return statement.offset(pagination.offset).limit(pagination.size)