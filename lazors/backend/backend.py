import logging

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
    player = {"name": "test"}
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
    player, created = ({"name": "test"}, True)
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
    return True
