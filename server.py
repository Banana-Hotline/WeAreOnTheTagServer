from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import jsonify
import json
from server_utils import *

db_connect = create_engine('sqlite:///laserdb.db')
app = Flask(__name__)
api = Api(app)

def get_player_info(player_id):
	conn = db_connect.connect()
	query = conn.execute("select user_id, display_name, display_image, stat_1, stat_2, stat_3 from PLAYER_INFO where user_id =%d " %int(player_id))
	result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
	return result

class players(Resource):
	def get(self):
		conn = db_connect.connect()
		query = conn.execute("select user_id, display_name, display_image from PLAYER_INFO;")
		result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result

class players_Info(Resource):
	def get(self, player_id):
		return get_player_info(player_id)

class add_players(Resource):
	def post(self):
		#print (request.is_json)
		content = request.get_json()
		conn = db_connect.connect()
		try:
			query = conn.execute("insert into PLAYER_INFO ( user_id, display_name, display_image, stat_1, stat_2, stat_3) values ('%s', '%s', '%s', 0, 0, 0) " %(content['user_id'], content['display_name'],content['display_image']))
		except Exception as e:

			return create_response('Fail','user_id is already present in the database')
		print query
		print (content)
		print (content['display_name'])
		print (content['display_image'])
		return create_response('Success','user was added to database')

class remove_players(Resource):
	def post(self):
		content = request.get_json()
		print ("Removing user %s from database." %content['user_id'])
		conn = db_connect.connect()
		try:
			query = conn.execute("delete from PLAYER_INFO where user_id = '%s'" %content['user_id'])
		except Exception as e:
			print e
			return create_response('Fail','Failed to remove user from database')
		return create_response('Success',"User %s has been removed from database" %content['user_id'])

class hit_notify(Resource):
	def post(self, player_id, attacker_id):
		if(player_id == attacker_id):
			return create_response('Fail',"Players can't tag themselves")
		content = request.get_json()
		print ("User %s was hit by %s." %(player_id, attacker_id))
		conn = db_connect.connect()
		try:
			victim_stats = get_player_info(player_id)['data'][0]
			attacker_stats = get_player_info(attacker_id)['data'][0]
			query = conn.execute("update PLAYER_INFO set stat_2 = '%s' where user_id = '%s'" %(int(victim_stats['stat_2']) + 1, player_id))
			query = conn.execute("update PLAYER_INFO set stat_1 = '%s' where user_id = '%s'" %(int(attacker_stats['stat_1']) + 1, attacker_id))
		except Exception as e:
			print e
			return create_response('Fail','Failed update hit in database')
		return create_response('Success', hit_notify_message_body %(victim_stats['display_name'], int(victim_stats['stat_2']) + 1, attacker_stats['display_name'], int(attacker_stats['stat_1']) + 1))

class sync_player_stats(Resource):
	def post(self,player_id):
		content = request.get_json()
		print ("Syncing User %s stats." %(player_id))
		conn = db_connect.connect()
		try:
			player_stats = get_player_info(player_id)['data'][0]
			if (int(player_stats['stat_3']) > int(content['shots'])):
				return create_response('Fail','Failed update stats')
			query = conn.execute("update PLAYER_INFO set stat_3 = '%s' where user_id = '%s'" %(int(content['shots']), player_id))
		except Exception as e:
			print e
			return create_response('Fail','Failed update hit in database')
		return create_response('Success',  "Synced User %s stats. Shots: %s" %(player_id, content['shots']))
	
api.add_resource(players, '/players') # Route_4
api.add_resource(players_Info, '/players/<player_id>') # Route_5
api.add_resource(add_players, '/players/add') # Route_5
api.add_resource(remove_players, '/players/remove') # Route_5
api.add_resource(hit_notify, '/hit/<player_id>/<attacker_id>') # Route_5
api.add_resource(sync_player_stats, '/stats/<player_id>') # Route_5



if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=5002,ssl_context=('certs/cert.pem', 'certs/key.pem'))