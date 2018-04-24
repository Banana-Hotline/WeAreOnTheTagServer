#!/usr/local/bin/python3

from minio import Minio
from minio.error import *
import os
import logging
import json


class Minio_DB:
    """
    This class simplifies abstracts the use of Lazors Minio DB
    Variables:
        minioClient: Minio instance used for connecting with Minio DB
    """
    def __init__(self):
        """
        Creates a Minio_DB instance and connects it to the Lazors Minio DB

        PARAMETERS:
            None
        RETURNS:
            self: Minio_DB instance connected to Lazors Minio_DB
        """
        self.connect()
    def connect(self):
        """
        Connects the current Minio_DB instance with a Minio instance

        PARAMETERS:
            None
        RETURNS:
            None
        """
        self.minioClient = Minio('play.minio.io:9000',
                                access_key='Q3AM3UQ867SPQQA43P2F',
                                secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                                secure=True)
    def makeBucket(self, bucket_name):
        """
        Makes a bucket in the Minio DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to create
        RETURNS:
            None
        """
        try:
            self.minioClient.make_bucket(bucket_name, location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            logging.info("AlreadyOwned")
            pass
        except BucketAlreadyExists as err:
            logging.info("AlreadyExists")
            raise
        except ResponseError as err:
            raise
        else:
            pass
    def write_to_bucket(self, bucket_name, obj_name, obj):
        """
        Writes a python dict to the Minio DB as a .json file

        PARAMETERS:
            bucket_name: name of the bucket you wish to create
            obj_name: name of the object you wish to create
            obj: dict object to be stored
        RETURNS:
            None
        """
        with open('tmp_{}.json'.format(obj_name), 'w') as outfile:  
            json.dump(obj, outfile)
        try:
            logging.info(self.minioClient.fput_object(bucket_name, '{}.json'.format(obj_name),
                                    'tmp_{}.json'.format(obj_name),
                                    content_type='application/json'))
            os.remove('tmp_{}.json'.format(obj_name))
        except ResponseError as err:
            logging.info(err)
    def read_from_bucket(self, bucket_name, obj_name):
        """
        Reads a python dict from the Minio DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to read
            obj_name: name of the object you wish to read
        RETURNS:
            obj: dict object read from Minio DB
        """
        try:
            self.minioClient.fget_object(bucket_name, '{}.json'.format(obj_name), 'tmp_{}.json'.format(obj_name)) 
            with open('tmp_{}.json'.format(obj_name)) as json_data:
                obj = json.load(json_data)
            os.remove('tmp_{}.json'.format(obj_name))
            return obj    
        except ResponseError as err:
            print(err)

    def remove_object(self, bucket_name,obj_name):
        """
        Removes an object from the Minio DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to remove the object from
            obj_name: name of the object you wish to remove
        RETURNS:
            None
        """
        try:
            self.minioClient.remove_object(bucket_name, '{}.json'.format(obj_name))
        except ResponseError as err:
            pass
    def remove_object_file(self, bucket_name,file_name):
        """
        Removes a file from the Minio DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to remove the object from
            file_name: name of the file you wish to remove
        RETURNS:
            None
        """
        try:
            self.minioClient.remove_object(bucket_name, file_name)
        except ResponseError as err:
            pass
    def remove_bucket(self, bucket_name):
        """
        Removes a bucket from the Minio DB

        PARAMETERS:
            bucket_name: name of the bucket you wish to remove
        RETURNS:
            None
        """
        try:
            self.minioClient.remove_bucket(bucket_name)
        except ResponseError as err:
            logging.info(err)
            raise
    def get_bucket_contents(self, bucket_name):
        """
        Returns the contents of a bucket

        PARAMETERS:
            bucket_name: name of the bucket you wish to read
        RETURNS:
            objects: generator containing the list of object files in the bucket
        """
        return self.minioClient.list_objects(bucket_name, recursive=True)
    def get_bucket_objects(self, bucket_name):
        """
        Returns the contents of a bucket

        PARAMETERS:
            bucket_name: name of the bucket you wish to read
        RETURNS:
            objects: generator containing the list of object in the bucket
        """
        objs = self.minioClient.list_objects(bucket_name, recursive=True)
        for obj in objs:
            object_name = obj.object_name
            if(object_name.endswith('.json')):
                obj.object_name = object_name[:-5]
                yield obj

#Run some UT on Minio_DB class
if(__name__ == '__main__'):
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--bucket', metavar='b', type=str, default = 'lazorsminiotest',
                        help='the bucket to test on')

    args = parser.parse_args()
    test = 1
    player = {
        "name": "Nintendo",
        "id": "64"
        }
    player_id = player["id"]
    bucket_name = args.bucket
    db = Minio_DB()
    print("Test {} -- Make Bucket".format(test))
    test += 1
    db.makeBucket(bucket_name)
    print("Passed: Bucket made\n")
    print("Test {} -- Write to Bucket".format(test))
    test += 1
    db.write_to_bucket(bucket_name, player_id, player)
    print("Passed: Object Written\n")
    print("Test {} -- List Bucket Objects".format(test))
    test += 1
    objs = db.get_bucket_objects(bucket_name)
    for obj in objs:
        print("\nBucket: {}\nObject Name: {}\nModified: {}\nETag: {}\nSize: {}\nContent Type: {}" \
                    .format(obj.bucket_name, obj.object_name, \
                    obj.last_modified, obj.etag, obj.size, obj.content_type))
    print("Passed: Objects Listed\n")
    print("Test {} -- List Bucket Contents".format(test))
    test += 1
    objs = db.get_bucket_contents(bucket_name)
    for obj in objs:
        print("\nBucket: {}\nObject File Name: {}\nModified: {}\nETag: {}\nSize: {}\nContent Type: {}" \
                    .format(obj.bucket_name, obj.object_name.encode('utf-8'), \
                    obj.last_modified, obj.etag, obj.size, obj.content_type))
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
    objs = db.get_bucket_contents(bucket_name)
    for obj in objs:
        db.remove_object_file(bucket_name, obj.object_name)
        print("Object {} removed".format(obj.object_name))
    print("Passed: All Objects Removed\n")
    print("Test {} -- Remove Bucket".format(test))
    test += 1
    db.remove_bucket(bucket_name)
    print("Passed: Bucket Removed\n")