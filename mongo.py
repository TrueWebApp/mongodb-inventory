#!/usr/bin/env python3

import json
import os
from argparse import ArgumentParser

from pymongo import MongoClient

# get mongo
mongo = MongoClient(os.getenv('INV_MONGO_URI'))
db = mongo.get_database(os.getenv('INV_MONGO_DB'))

# define parser
parser = ArgumentParser()
parser.add_argument('--list',
                    action="store_true",
                    help='Print a JSON-encoded hash or dictionary '
                         'that contains all the groups to be managed')
parser.add_argument('--host',
                    metavar='hostname',
                    nargs=1,
                    help='Print either an empty JSON hash/dictionary, '
                         'or a hash/dictionary of variables')


def main():
    args = parser.parse_args()
    if args.list:
        return get_inventory()
    if args.host:
        return get_host(args.host[0])
    return {}


def get_inventory():
    """ Get all inventory. """
    inv = get_data('groups')
    if os.getenv('INV_INCLUDE_META'):
        inv['_meta'] = {'hostvars': get_data('hosts')}
    return inv


def get_host(name):
    """ Get dict with one host variables. """
    col = db.get_collection('hosts')
    data = col.find_one({'name': name}) or {}
    return _prepare(data)


def get_data(collection):
    """ Get all items from collection and return object {name: dict_with_other_vars}. """
    col = db.get_collection(collection)
    return {data['name']: _prepare(data) for data in col.find()}


def _prepare(data: dict):
    """ Remove fields `_id` and `name` and return data. """
    return {k: v for k, v in data.items() if k not in ('_id', 'name')}


if __name__ == "__main__":
    result = main()
    print(json.dumps(result))
    mongo.close()
