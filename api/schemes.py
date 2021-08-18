from humps import camelize
from pydantic import BaseModel, constr


class ToCamel(BaseModel):
    class Config:
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return camelize(string)


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserName(BaseModel):
    username: constr(min_length=3, max_length=254)


class UserSet(UserName):
    password: constr(min_length=6, max_length=254)


class UserGet(UserName):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
