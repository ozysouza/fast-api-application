from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(
        sa_column=Column(Boolean, server_default=text('true'), nullable=False)
    )
    created_at: Optional[datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    )
