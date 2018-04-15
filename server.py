from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import jsonify
import json
import server_utils

db_connect = create_engine('sqlite:///laserdb.db')
app = Flask(__name__)
api = Api(app)


class players(Resource):
	def get(self):
		conn = db_connect.connect()
		query = conn.execute("select user_id, display_name, display_image from PLAYER_INFO;")
		result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result

class players_Info(Resource):
	def get(self, player_id):
		conn = db_connect.connect()
		query = conn.execute("select user_id, display_name, display_image from PLAYER_INFO where user_id =%d " %int(player_id))
		result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result

class add_players(Resource):
	def post(self):
		#print (request.is_json)
		content = request.get_json()
		conn = db_connect.connect()
		try:
			query = conn.execute("insert into PLAYER_INFO ( user_id, display_name, display_image) values ('%s', '%s', '%s') " %(content['user_id'], content['display_name'],content['display_image']))
		except Exception as e:

			return create_respone('Fail','user_id is already present in the database')
		print query
		print (content)
		print (content['display_name'])
		print (content['display_image'])
		return create_respone('Success','user was added to database')

class remove_players(Resource):
	def post(self):
		content = request.get_json()
		print ("Removing user %s from database." %content['user_id'])
		conn = db_connect.connect()
		try:
			query = conn.execute("delete from PLAYER_INFO where user_id = '%s'" %content['user_id'])
		except Exception as e:
			print e
			return server_utils.create_respone('Fail','Failed to remove user from database')
		return server_utils.create_respone('Success',"User %s has been removed from database" %content['user_id'])

api.add_resource(players, '/players') # Route_4
api.add_resource(players_Info, '/players/<player_id>') # Route_5
api.add_resource(add_players, '/players/add') # Route_5
api.add_resource(remove_players, '/players/remove') # Route_5


if __name__ == '__main__':
	app.debug=True
	app.ssl_context=('cert.pem', 'key.pem')
	app.run(host='0.0.0.0',port=5002)
