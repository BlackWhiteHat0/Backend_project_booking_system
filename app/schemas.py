from pydantic import BaseModel

class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:int
    is_active:bool

    class Config:
        from_atributes = True

class ItemBase(BaseModel):
    title:str
    description:str | None=None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id:int
    owner_id:int

    class Config:
        from_attributes = True