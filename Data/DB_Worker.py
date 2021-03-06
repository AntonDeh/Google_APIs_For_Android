# title:           	DB_Worker.py
# description:
# author:          	Roman Tochony
# date:            	20.2.2019
# version:          1.0
# notes:
# python_version:   Python 3.7.2

from WebScrape import Config
from Data.DataManager import *
import pymongo


class MongoDB:
    """Object initiator function"""
    def __init__(self):
        try:
            print('Connecting to the DB - {} {}.{}'.format(Config.host_DB, Config.DB_name, Config.DB_collection))
            self.client = pymongo.MongoClient(Config.host_DB)
            self.db_name = self.client[Config.DB_name]
            self.db_collection = self.db_name[Config.DB_collection]
        except Exception as e:
            raise Exception("Something went wrong during DB connection:{}".format(e))

    def fill_collections_to_db(self, collection_list):
        """This function will inject ito the DB list of collections"""
        container = Container()
        try:
            collection = self.db_collection
            collection_list = [x for x in collection_list if (not self._is_collection_exist(x))
                               or container.is_valid_collection(x)]
            if len(collection_list) > 0:
                collection.insert_many(collection_list)
        except Exception as e:
            raise Exception("Something went wrong during DB insertion:{}".format(e))

    def read_collections_from_db(self):
        """This function will load collections from DB and return list of them"""
        try:
            temp = []
            collection = self.db_collection
            temp.extend(collection.find())
            return temp
        except Exception as e:
            raise Exception("Something went wrong during DB reading:{}".format(e))

    def find_invalid_collections_from_db(self):
        """This function will find collections from DB and return list of them"""
        try:
            collection = self.db_collection
            temp = [x for x in collection.find({'is_valid': False})]
            return temp
        except Exception as e:
            raise Exception("Something went wrong during DB reading:{}".format(e))

    def set_validity_for_collections(self, collection_list, bool_val):
        """This function will get list of collection and set the bit is_valid"""
        try:
            collection = self.db_collection
            for i in collection_list:
                if self._is_collection_exist(i):
                    collection.update_many({"sha": i['sha']}, {"$set": {"is_valid": bool_val}})
        except Exception as e:
            raise Exception("Something went wrong during value updating collections:{}".format(e))

    def _is_collection_exist(self, single_collection):
        """This helper function will prevent duplicates in DB"""
        collection = self.db_collection
        if collection.find({"sha": single_collection['sha']}).count() > 0:
            return True
        return False
