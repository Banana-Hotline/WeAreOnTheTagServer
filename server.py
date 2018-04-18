from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import jsonify
import json
from server_utils import *
		# Import Minio library.
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

app = Flask(__name__)
api = Api(app)

class players(Resource):
	def get(self):
		return create_response('Fail','Not currently implemented')

class players_Info(Resource):
	def get(self, player_id):
		return create_response('Fail','Not currently implemented')

class add_players(Resource):
	def post(self):
<<<<<<< HEAD
		return create_response('Fail','Not currently implemented')
=======
		#print (request.is_json)
		content = request.get_json()
		conn = db_connect.connect()
		try:
			query = conn.execute("insert into PLAYER_INFO ( user_id, display_name, display_image) values ('%s', '%s', '%s') " %(content['user_id'], content['display_name'],content['display_image']))
		except Exception as e:
			print e
			return create_response('Fail','user_id is already present in the database')
		print query
		print (content)
		print (content['display_name'])
		print (content['display_image'])
		return create_response('Success','user was added to database')
>>>>>>> 6207ff21bd3668a639655d4203188950cae00a2d

class remove_players(Resource):
	def post(self):
		return create_response('Fail','Not currently implemented')

class hit_notify(Resource):
	def post(self, player_id, attacker_id):
		return create_response('Fail','Not currently implemented')

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
		try:
			print(err)
			minioClient.remove_bucket("maylogs")
		except ResponseError as err:
			print(err)
		return create_response('Fail','Not currently implemented')

api.add_resource(players, '/players') # Route_4
api.add_resource(players_Info, '/players/<player_id>') # Route_5
api.add_resource(add_players, '/players/add') # Route_5
api.add_resource(remove_players, '/players/remove') # Route_5
api.add_resource(hit_notify, '/hit/<player_id>/<attacker_id>') # Route_5
api.add_resource(minio_test, '/minio') # Route_5



if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=5002,ssl_context=('certs/cert.pem', 'certs/key.pem'))
