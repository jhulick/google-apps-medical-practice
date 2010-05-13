""" This module provdes helpers.
  Author: Jeremy Hulick
  Date: 09-30-2009
  Last Modified: 02-14-2010
"""

import time, datetime, hashlib, models
from google.appengine.ext import db
from models import User

#-----------------------------------------------------------------------------
# GENERAL JSON HELPERS
#-----------------------------------------------------------------------------
def apply_json_to_model_instance(model, jobj):
  """This is the generic method to apply the given json to the given model"""
  for key in model.properties():
    setattr(model, key, jobj[key] if jobj.has_key(key) else None)
  
  return model  


def build_list_json(list):
  """This method will build the users list in JSON"""
  users_json = []
  for user in list:
    user_json = { "id": "%s" % user.key().id_or_name(),
      "name": user.name
    }
  
    users_json.append(user_json)
  return users_json

def generateAuthToken():
  """This method generates the authToken for a user every time they login"""
  return hashlib.sha1("This--is--the--authToken--%s" % time.mktime(datetime.datetime.utcnow().timetuple())).hexdigest()


