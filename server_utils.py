
def create_response(result, message):
    return {"data":{'Result':result,'Message':message}}

hit_notify_message_body = \
"""The number of hits has been updated in the database.
User %s has been struck %s times. 
User %s has %s tags
"""
