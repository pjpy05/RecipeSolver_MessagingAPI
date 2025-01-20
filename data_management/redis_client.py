import redis
from typing import Any, Optional
# from redis_user import RedisUser  # RedisUserを別ファイルからインポート
from config import REDIS_URL
import json

class RedisClient:
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, db: int = 0):
        """
        Redisクライアントの初期化。
        環境変数 `REDIS_URL` が設定されている場合は優先的に使用。
        """
        # Render環境では REDIS_URL が設定されていることが多い
        redis_url = REDIS_URL
        if redis_url:
            self.client = redis.StrictRedis.from_url(redis_url, decode_responses=True)
        else:
            # 環境変数がない場合は引数から接続設定を取得
            self.client = redis.StrictRedis(
                host=host or "localhost",
                port=port or 6379,
                db=db,
                decode_responses=True
            )
    
    # LIFFで使用
    def get_hash_as_json(self, hash_name: str) -> str:
        """
        指定したハッシュ名に関連する全てのフィールドと値をJSON形式で取得。
        
        :param hash_name: Redisに保存されたハッシュの名前
        :return: JSON形式の文字列
        """
        # ハッシュ型データを取得
        hash_data = self.client.hgetall(hash_name)
        
        # JSON形式の文字列に変換
        return json.dumps(hash_data, ensure_ascii=False)
    
    # LIFFで使用
    def set_hash_from_json(self, hash_name: str, json_data: str) -> None:
        """
        JSONデータを受け取り、それをRedisのハッシュとしてセットする。
        
        :param hash_name: Redisに保存するハッシュの名前
        :param json_data: JSON形式の文字列
        """
        try:
            # JSON文字列を辞書に変換
            data = json.loads(json_data)
            if not isinstance(data, dict):
                raise ValueError("JSONデータは辞書形式でなければなりません。")
            
            # Redisにハッシュとしてセット
            self.client.hset(hash_name, mapping=data)
        except json.JSONDecodeError as e:
            raise ValueError(f"無効なJSON形式です: {e}")