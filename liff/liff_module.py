from data_management.redis_client import RedisClient

redis=RedisClient()
redis_client=redis.client

# LIFFにデータを渡す
def get_context(user_id):
    redis_json=redis.get_hash_as_json(user_id)
    return redis_json

# LIFFからのデータを保存する
def set_context(user_id,json_data):
    redis.set_hash_from_json(user_id, json_data)