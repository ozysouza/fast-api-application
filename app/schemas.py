from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """Schema for the response data of a User object."""
    id: int
    email: EmailStr
    created_at: datetime  # Date and time when the user was created.


class PostBase(BaseModel):
    """Base schema for a Post object, containing core fields."""
    title: str  # Title of the post.
    content: str  # Content/body of the post.
    published: bool = True  # Publication status, defaults to True.


class PostCreate(PostBase):
    """Schema for creating a new Post. Inherits from PostBase."""
    pass


class PostResponse(PostBase):
    """Schema for the response data of a Post object."""
    id: int  # Unique identifier for the post.
    created_at: datetime  # Date and time when the post was created.
    owner: UserResponse  # Details of the user who created the post.


class PostVoteOut(BaseModel):
    Post: PostResponse
    votes: int


class UserCreate(BaseModel):
    """Schema for creating a new User."""
    email: EmailStr  # Email of the user.
    password: str  # Password for the user account (stored securely).


class UserLogin(BaseModel):
    """Schema for logging in a User."""
    email: EmailStr  # Email of the user attempting to log in.
    password: str  # Password for the user account.


class Token(BaseModel):
    """Schema for the access token returned after authentication."""
    access_token: str  # JWT access token.
    token_type: str  # Bearer type of token


class TokenData(BaseModel):
    """Schema for token data extracted from the access token."""
    id: Optional[int] = None  # Optional user ID from the token data.


class Vote(BaseModel):
    """Schema for voting on a post."""
    post_id: int  # ID of the post being voted on.
    dir: Literal[0, 1]  # Voting direction: 1 for upvote, 0 for downvote.
