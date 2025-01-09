from data_management.redis_client import RedisClient

redis=RedisClient()
redis_client=redis.client

# LIFFにデータを渡す
def liff(user_id):
    redis_json=redis.get_hash_as_json(user_id)
    return redis_json
