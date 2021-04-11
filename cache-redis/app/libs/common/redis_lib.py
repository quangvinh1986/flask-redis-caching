import json
from app.extensions import redis_db
from flask import current_app


def save_all_to_redis(result, key, time_expire=21600):
    try:
        my_hash = redis_db.Hash(key)
        my_hash[key] = json.dumps(result)
        if time_expire:
            redis_db.expire(key, time_expire)
    except Exception as ex:
        current_app.logger.warning("save_all_to_redis for {} fail {}".format(key, ex.__str__()))


def get_all_from_redis(key):
    try:
        my_hash = redis_db.Hash(key)
        if my_hash:
            my_dict = my_hash[key]
            if my_dict:
                return json.loads(my_dict)
            else:
                return {}
        else:
            return {}
    except Exception as ex:
        current_app.logger.warning("get_all_from_redis by {} fail {} ".format(key, ex.__str__()))
        return {}


def save_data_text(key, value, time_expire=21600):
    my_hash = redis_db.Hash(key)
    my_hash[key] = value
    if time_expire:
        redis_db.expire(key, time_expire)


def get_data_text(key):
    if redis_db.Hash(key):
        my_hash = redis_db.Hash(key)
        return my_hash[key].decode("utf-8")
    else:
        return ""
