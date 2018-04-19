class minio_test(Resource):
    def post(self):

        # Initialize minioClient with an endpoint and access/secret keys.
        minioClient = Minio('play.minio.io:9000',
                            access_key='Q3AM3UQ867SPQQA43P2F',
                            secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                            secure=True)

        # Make a bucket with the make_bucket API call.
        try:
            minioClient.make_bucket("maylogs", location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            print "AlreadyOwned"
            pass
        except BucketAlreadyExists as err:
            print "AlreadyExists"
            pass
        except ResponseError as err:
            raise
        else:
            # Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
            try:
                minioClient.fput_object('maylogs', 'pumaserver_debug.log', './laserdb.db')
            except ResponseError as err:
                print(err)
        # List all object paths in bucket that begin with my-prefixname.
        objects = minioClient.list_objects('maylogs', recursive=True)
        for obj in objects:
            print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
                obj.etag, obj.size, obj.content_type)
            
            minioClient.remove_object(obj.bucket_name, obj.object_name)
        # Remove an object.
        try:
            minioClient.remove_object('maylogs', 'pumaserver_debug.log')
        except ResponseError as err:
            pass
        try:
            print(err)
            minioClient.remove_bucket("maylogs")
        except ResponseError as err:
            print(err)
        return create_response('Fail','Not currently implemented')