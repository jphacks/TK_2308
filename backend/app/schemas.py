from pydantic import BaseModel


class Sample(BaseModel):
    text: str

    class Config:
        orm_mode = True
