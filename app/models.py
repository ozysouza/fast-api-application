from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlmodel import Field, SQLModel, Relationship


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
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)
    owner: Optional["User"] = Relationship(back_populates="posts")


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    )
    posts: list["Post"] = Relationship(back_populates="owner")


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE", primary_key=True, nullable=False)
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE", primary_key=True, nullable=False)

    post: Optional["Post"] = Relationship(sa_relationship_kwargs={"lazy": "select"})
    user: Optional["Post"] = Relationship(sa_relationship_kwargs={"lazy": "select"})
