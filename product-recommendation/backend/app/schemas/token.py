from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" # デフォルト値

class TokenData(BaseModel): # トークンペイロードの検証用 (任意)
    username: str | None = None
    # id: int | None = None # sub に id を使う場合