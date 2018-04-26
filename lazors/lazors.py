#!/usr/local/bin/python3
import connexion
import gevent.ssl
import logging
import backend

SSL_PATHS = ('etc/tls/server.crt', 'etc/tls/server.key')


def get_players():
    """
    Get a list of all players

    PARAMETERS:
        None
    RETURNS:
        list[player]
    """
    players = backend.get_players()
    return players

def get_player(player_id):
    """
    Get a player

    PARAMETERS:
        player_id: player id
    RETURNS:
        player
    """
    player = backend.get_player(player_id=player_id)
    if player is None:
        return (None,404)
    return player

def put_player(player_id, player):
    """
    Create/Update a player

    PARAMETERS:
        player_id: player id
        player:
            name: The player name
            id (OPTIONAL): The id
    RETURNS:
        player
    """
    player, created = backend.put_player(player_id=player_id, player=player)
    if created:
        return (player, 201)
    else:
        return (player, 200)

def delete_player(player_id):
    """
    Deletes a player

    PARAMETERS:
        player_id: player id
    RETURNS:
        player
    """
    deleted = backend.delete_player(player_id=player_id)
    return deleted

logging.basicConfig(level=logging.INFO)
app = connexion.App("Lazors")
app.add_api('etc/apispec/swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    ssl_context = gevent.ssl.SSLContext(gevent.ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(*SSL_PATHS)
    app.run(port=8080, server='gevent', ssl_context=ssl_context)