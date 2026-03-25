from pydantic import BaseModel


class AdAccountCreate(BaseModel):
    client_id: int
    platform: str
    account_id: str
    access_token: str


class AdAccountResponse(BaseModel):
    id: int
    client_id: int
    platform: str
    account_id: str

    class Config:
        from_attributes = True