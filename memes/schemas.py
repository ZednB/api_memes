# memes/schemas.py
from pydantic import BaseModel
from typing import Optional


class MemeBase(BaseModel):
    title: str
    description: Optional[str] = None


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass


class Meme(MemeBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True
