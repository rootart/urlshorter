import random
from hashlib import md5
import uuid
import shortuuid
import sys

import pymongo
from pymongo import Connection
from pymongo import ASCENDING, DESCENDING


ALPHABET = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def gen_sample(alphabet, number=6):
    list = random.sample(alphabet, number)
    return ''.join(list)


def md5_url(url):
    _hash = md5()
    _hash.update(url)
    return  _hash.hexdigest()


def gen_uuid(url):
    data = str(uuid.uuid1())
    data = data.split('-')[-1]
    return data


def gen_shortuuid(url):
    '''
    Actual shortuuid is external project
    find more information here https://github.com/stochastic-technologies/shortuuid/
    '''
    return shortuuid.uuid(url)


def update_mongo():
    connection = Connection()
    db = connection.urlshort
    collection = db.url_2

    # Generate  pseudo unique hashes
    for item in collection.find():
        url = item['url']
        item.update(
            sample = gen_sample(ALPHABET),
            md5 = md5_url(url),
            uuid = gen_uuid(url),
            shortuuid = gen_shortuuid(url.encode())
        )
        collection.save(item)

    # Create index
    print "[!] Start creating index"
    collection.create_index([("sample", DESCENDING), ("uuid", ASCENDING),
        ("shortuuid", ASCENDING)])
    print "[!]  Index created"

    # Check for unique items
    collection = db.url_2
    for item in collection.find():
        count = collection.find({'sample': item['sample']}).count()
        while count > 1:
            print "Dublication"
            item.update(sample=gen_sample(ALPHABET))
            collection.save(item)


if __name__ == '__main__':
    if sys.argv:
        for arg in sys.argv[1:]:
            print arg +" -> "+ gen_sample(ALPHABET)
    if len(sys.argv) == 1:
        update_mongo()
