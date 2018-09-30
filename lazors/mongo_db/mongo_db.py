#!usr/local/bin/python3

from pymongo import MongoClient
import os
import logging
import json


class Mongo_DB:
    """
    This class simplifies abstracts the use of Lazors Mongo DB
    Variables:
        mongoClient: Mongo instance used for connecting with Mongo DB
    """
    def __init__(self):
        """
        Creates a Mongo_DB instance and connects it to the Lazors Mongo DB

        PARAMETERS:
            None
        RETURNS:
            self: Mongo_DB instance connected to Lazors Mongo_DB
        """
        self.connect()
    def connect(self):
        """
        Connects the current Mongo_DB instance with a Mongo instance

        PARAMETERS:
            None
        RETURNS:
            None
        """
        self.mongoClient = MongoClient('mongodb://localhost:27017/')
        self.db = self.mongoClient.db
    def make_bucket(self, bucket_name):
        """
        Makes a bucket in the Mongo DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to create
        RETURNS:
            None
        """
    def write_to_bucket(self, bucket_name, obj_name, obj):
        """
        Writes a python dict to the Mongo DB as a .json file

        PARAMETERS:
            bucket_name: name of the bucket you wish to create
            obj_name: name of the object you wish to create
            obj: dict object to be stored
        RETURNS:
            None
        """
        write_obj = {"_name": obj_name, "_object" : obj}
        filter = {"_name" : obj_name}
        if self.db[bucket_name].count(filter):
            self.db[bucket_name].find_one_and_replace(filter, write_obj)
        else:
            self.db[bucket_name].insert_one(write_obj)
    def read_from_bucket(self, bucket_name, obj_name):
        """
        Reads a python dict from the Mongo DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to read
            obj_name: name of the object you wish to read
        RETURNS:
            obj: dict object read from Mongo DB
        """
        obj = self.db[bucket_name].find_one({"_name" : obj_name})
        if obj is None:
            return None
        else:
            return obj["_object"]

    def remove_object(self, bucket_name, obj_name):
        """
        Removes an object from the Mongo DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to remove the object from
            obj_name: name of the object you wish to remove
        RETURNS:
            None
        """
        self.db[bucket_name].delete_one({"_name" : obj_name})

    def remove_object_file(self, bucket_name,file_name):
        """
        Removes a file from the Mongo DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to remove the object from
            file_name: name of the file you wish to remove
        RETURNS:
            None
        """
        self.db[bucket_name].delete_one({"_name" : file_name[:-5]})
    def remove_bucket(self, bucket_name):
        """
        Removes a bucket from the Mongo DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to remove
        RETURNS:
            None
        """
        self.db.drop_collection(bucket_name)
    def get_bucket_contents(self, bucket_name):
        """
        Returns the contents of a bucket

        PARAMETERS:
            bucket_name: name of the bucket you wish to read
        RETURNS:
            objects: generator containing the list of object files in the bucket
        """
        for obj in self.db[bucket_name].find():
            yield obj["_object"]
    def get_bucket_objects(self, bucket_name):
        """
        Returns the contents of a bucket

        PARAMETERS:
            bucket_name: name of the bucket you wish to read
        RETURNS:
            objects: generator containing the list of object in the bucket
        """
        return self.db[bucket_name].find()

#Run some UT on Mongo_DB class
if(__name__ == '__main__'):
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--bucket', metavar='b', type=str, default = 'lazorsmongotest',
                        help='the bucket to test on')

    args = parser.parse_args()
    test = 1
    player = {
        "name": "Nintendo",
        "id": "64"
        }
    player_id = player["id"]
    player2 = {
        "name": "MamBO Number 5!",
        "id": "12345"
        }
    player_id2 = player2["id"]
    bucket_name = args.bucket
    db = Mongo_DB()
    print("Test {} -- Make Bucket".format(test))
    test += 1
    db.make_bucket(bucket_name)
    print("Passed: Bucket made\n")
    print("Test {} -- Write to Bucket".format(test))
    test += 1
    db.write_to_bucket(bucket_name, player_id, player)
    db.write_to_bucket(bucket_name, player_id2, player2)
    print("Passed: Object Written\n")
    print("Test {} -- List Bucket Objects".format(test))
    test += 1
    objs = db.get_bucket_objects(bucket_name)
    for obj in objs:
        print(obj)
    print("Passed: Objects Listed\n")
    print("Test {} -- List Bucket Contents".format(test))
    test += 1
    objs = db.get_bucket_contents(bucket_name)
    for obj in objs:
        print(obj)
    print("Passed: Objects Files Listed\n")
    print("Test {} -- Read from Bucket".format(test))
    test += 1
    print(db.read_from_bucket(bucket_name, player_id))
    print("Passed: Object Read\n")
    print("Test {} -- Remove Object".format(test))
    test += 1
    db.remove_object(bucket_name, player_id)
    print("Passed: Object Removed\n")
    print("Test {} -- Remove All Objects".format(test))
    test += 1
    print("Contents Before Remove")
    objs = db.get_bucket_contents(bucket_name)
    for obj in objs:
        print(obj)
    objs = db.get_bucket_contents(bucket_name)
    for obj in objs:
        db.remove_object(bucket_name,obj["_name"])
        print("Object {} removed".format(obj["_name"]))
    print("Contents After Remove")
    objs = db.get_bucket_contents(bucket_name)
    for obj in objs:
        print(obj)
    print("Passed: All Objects Removed\n")
    print("Test {} -- Remove Bucket".format(test))
    test += 1
    db.remove_bucket(bucket_name)
    print("Passed: Bucket Removed\n")