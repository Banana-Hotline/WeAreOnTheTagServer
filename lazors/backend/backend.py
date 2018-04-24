import logging
from minio_db import Minio_DB

db = Minio_DB()
db.makeBucket("players")
def get_players():
    """
    Get a list of all players

    PARAMETERS:
        None
    RETURNS:
        list[player]
    """
    logging.info("Getting list of all players")
    players = []
    player_objs = db.get_bucket_contents("players")
    for player in player_objs:
        players.append(get_player(player.object_name))
    return players

def get_player(player_id):
    """
    Get a player

    PARAMETERS:
        player_id: player id
    RETURNS:
        player
    """
    logging.info("Getting player {}".format(player_id))
    player = db.read_from_bucket("players", player_id)
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
        player, created (was it created)
    """
    logging.info("Put player: {}".format(player_id))
    logging.info("Player info: {}".format(player))
    if(player_id != player['id']):
        player, created = ({"name": player['name']}, False)
        return (player, created)
    db.makeBucket("players")
    db.write_to_bucket("players", player_id, player)
    player, created = ({"name": player['name']}, True)
    return (player, created)

def delete_player(player_id):
    """
    Deletes a player

    PARAMETERS:
        player_id: player id
    RETURNS:
        player
    """
    logging.info("Deleting player {}".format(player_id))
    db.remove_object("players", player_id)

    return True
