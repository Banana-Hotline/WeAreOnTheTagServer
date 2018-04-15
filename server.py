from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import jsonify
import json

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
		print ("fuck you")
		#print (request.is_json)
		content = request.get_json()
		print (content)
		print (content['display_name'])
		print (content['display_image'])
		return 'JSON posted'


api.add_resource(players, '/players') # Route_4
api.add_resource(players_Info, '/players/<player_id>') # Route_5
api.add_resource(add_players, '/players/add') # Route_5


if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=5002)
	 