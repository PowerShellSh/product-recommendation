from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.user import User
from app.models.purchase import Purchase
from app.db.base_class import Base  # SQLAlchemy Base クラス
from app.db.session import engine   # SQLAlchemy Engine

# --- 初期データ ---
initial_products = [
    {"name": "スマートフォン", "description": "最新のスマートフォン", "price": 89800, "category": "電化製品", "image_url": "https://fakestoreapi.com/img/71kWymZ+c+L._AC_SX679_.jpg"},
    {"name": "ゲーミングノートパソコン", "description": "高性能ゲーミングノートPC、最新のグラフィックカード搭載", "price": 198000, "category": "電化製品", "image_url": "https://fakestoreapi.com/img/81Zt42ioCgL._AC_SX679_.jpg"},
    {"name": "ヘッドフォン", "description": "ノイズキャンセリング機能付き", "price": 34800, "category": "オーディオ", "image_url": "https://fakestoreapi.com/img/61IBBVJvSDL._AC_SY879_.jpg"},
    {"name": "電気ケトル", "description": "1L容量のコンパクト電気ケトル", "price": 4500, "category": "キッチン家電", "image_url": "https://fakestoreapi.com/img/51Y5NI-I5jL._AC_UX679_.jpg"},
    {"name": "スマートウォッチ", "description": "多機能スマートウォッチ、心拍センサー搭載", "price": 23800, "category": "電化製品", "image_url": "https://fakestoreapi.com/img/81gjAxhHpnL._AC_SL1500_.jpg"},
    {"name": "ブレンダー", "description": "多用途ブレンダー、スムージー作りに最適", "price": 9800, "category": "キッチン家電", "image_url": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_QL65_ML3_.jpg"},
    {"name": "タブレット", "description": "高解像度ディスプレイ搭載のタブレット端末", "price": 55000, "category": "電化製品", "image_url": "https://fakestoreapi.com/img/81QpkIctqPL._AC_SX679_.jpg"},
    {"name": "スピーカー", "description": "高音質ワイヤレススピーカー", "price": 12500, "category": "オーディオ", "image_url": "https://fakestoreapi.com/img/61mtL65D4cL._AC_SX679_.jpg"},
    {"name": "マウス", "description": "ゲーミングマウス、プログラマブルボタン付き", "price": 7600, "category": "コンピュータ周辺機器", "image_url": "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg"},
    {"name": "キーボード", "description": "メカニカルキーボード、RGBライティング付き", "price": 13500, "category": "コンピュータ周辺機器", "image_url": "https://fakestoreapi.com/img/51eg55uWmdL._AC_UX679_.jpg"}
]

initial_users = [
    {"username": "user1", "email": "user1@example.com"}, # hashed_password は None または実際のハッシュ値
    {"username": "user2", "email": "user2@example.com"},
    {"username": "user3", "email": "user3@example.com"},
    {"username": "user4", "email": "user4@example.com"},
    {"username": "user5", "email": "user5@example.com"},
    {"username": "user6", "email": "user6@example.com"},
    {"username": "user7", "email": "user7@example.com"},
    {"username": "user8", "email": "user8@example.com"}
]

initial_purchases = [
    {"user_id": 1, "product_id": 1, "quantity": 1, "rating": 5},
    {"user_id": 1, "product_id": 2, "quantity": 1, "rating": 4},
    {"user_id": 2, "product_id": 1, "quantity": 1, "rating": 3},
    {"user_id": 2, "product_id": 3, "quantity": 1, "rating": 4},
    {"user_id": 3, "product_id": 4, "quantity": 1, "rating": 5},
    {"user_id": 3, "product_id": 5, "quantity": 1, "rating": 4},
    {"user_id": 4, "product_id": 3, "quantity": 1, "rating": 3},
    {"user_id": 4, "product_id": 2, "quantity": 1, "rating": 5},
    {"user_id": 5, "product_id": 6, "quantity": 1, "rating": 4},
    {"user_id": 5, "product_id": 7, "quantity": 1, "rating": 5},
    {"user_id": 6, "product_id": 8, "quantity": 1, "rating": 3},
    {"user_id": 6, "product_id": 1, "quantity": 1, "rating": 4},
    {"user_id": 7, "product_id": 10, "quantity": 1, "rating": 5},
    {"user_id": 7, "product_id": 9, "quantity": 1, "rating": 3},
    {"user_id": 8, "product_id": 8, "quantity": 1, "rating": 4},
    {"user_id": 8, "product_id": 6, "quantity": 1, "rating": 5}
]
# --- 初期データここまで ---


def init_db(db: Session) -> None:
    """
    データベースの初期化（テーブル作成と初期データ投入）を行う。
    冪等性を考慮し、既にデータが存在する場合はデータ投入をスキップする。
    """
    print("Initializing database...")

    # テーブル作成（存在しない場合のみ）
    try:
        print("Creating tables...")
        # Session から bind を取得するのがより安全な場合がある
        Base.metadata.create_all(bind=db.get_bind())
        # または Base.metadata.create_all(bind=engine)
        print("Tables created (if they didn't exist).")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # テーブル作成失敗時は続行しない方が良いかもしれない
        raise

    # --- 冪等性チェック ---
    print("Checking for existing data...")
    # 最初のユーザーが存在するかどうかで、初期データ投入済みか判断（より確実な方法も検討可）
    first_user = db.query(User).filter(User.email == initial_users[0]['email']).first()

    if not first_user:
        print("No existing user data found. Adding initial data...")

        # --- 初期データ投入 ---
        try:
            # Product データ
            print("Adding products...")
            for product_data in initial_products:
                product = Product(**product_data)
                db.add(product)
            # 必要なら db.flush()

            # User データ (実際のアプリではパスワードハッシュ化が必要)
            print("Adding users...")
            for user_data in initial_users:
                # User モデルに hashed_password がなければ引数から削除
                user_create_data = user_data.copy()
                if 'hashed_password' not in User.__table__.columns:
                     user_create_data.pop('hashed_password', None) # Userモデルに合わせて削除

                user = User(**user_create_data)
                db.add(user)
            db.flush() # User の ID を確定させるために Flush

            # Purchase データ (User ID が確定している必要がある)
            print("Adding purchases...")
            # UserとProductのIDを確定させた後で投入するのが確実だが、
            # 今回は initial_purchases のIDがそのまま使える前提
            for purchase_data in initial_purchases:
                purchase = Purchase(**purchase_data)
                db.add(purchase)

            print("Committing initial data...")
            db.commit()
            print("Initial data committed.")

        except Exception as e:
            print(f"Error during data insertion: {e}")
            print("Rolling back initial data insertion.")
            db.rollback() # エラー発生時はロールバック
            raise # エラーを再発生させる

    else:
        print("Initial user data already exists. Skipping data insertion.")
        # データ投入をスキップした場合も、セッションの状態をクリーンにするため rollback() を呼ぶ
        db.rollback()

    print("Database initialization finished.")