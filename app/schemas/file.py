from pydantic import BaseModel, Field

class File(BaseModel):
    id: str = Field(None, example='01FFFJR2ZW88G67AF5DJT85NMQ')
    upload_epoch_ms: int = Field(None, example=1234567890123)
    name: str = Field(None, example='example.txt')
    size: int = Field(0, example=12345)
    human_readable_size: str = Field(None, example='12.1 KB')

    class Config:
        orm_mode = True
