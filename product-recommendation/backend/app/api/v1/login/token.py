from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models # models パッケージからインポート
from app import schemas
from app.api import deps
from app.core.security import verify_password, create_access_token # セキュリティ関数をインポート
from app.core.config import settings # 有効期限設定などをインポート
from datetime import timedelta

router = APIRouter()

@router.post("/token", response_model=schemas.Token) # パスはルーターのprefixに依存
def login_for_access_token(
    db: Session = Depends(deps.get_db), # 正しい get_db を指定
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # 401 Unauthorized ステータス
            detail="Incorrect username or password",    # エラー詳細メッセージ
            headers={"WWW-Authenticate": "Bearer"},      # レスポンスヘッダー
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}