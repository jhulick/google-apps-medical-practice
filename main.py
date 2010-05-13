#!/usr/bin/env python

""" Prupose: To serve tasks & project to SG's Sproutcore Tasks application.
    Author: Joshua Holt
    Date: 09-30-2009
    Last Modified: 02-14-2010
    
    ********* NOTE(2) ***********
    I added a nasty hack that I am not proud of on line #84
    
    ********* SOLVED *************
    
    I've solved the issue below.. I had forgotten that python and a builtin
    function "setattr(obj, attr, val)". If you want to see how it DRYed up
    the code you can look through the commit log.
    
    
    ********* NOTE ***************
    This Code is not DRY it has been years since I've touched python
     ruby spoiled me :)
     
     Trying figure out a way to loop through model_instance.properties()
     and actually be able to use that to set the  model instance attrs
     
     Currently I am only able to do the 1/2 of the DRYing up that I want
     to do.
     
     This is what I am trying to do in my helpers module:
     
     def apply_json_to_model_instance(model, json):
       props = model.properties()
       for key in props:
         if json.has_key(key):
           model.key = json[key]
        
        model.put()
     
     
     But it seems that you cannot do this b/c I remember that you cannot
     specify an object's attribute as a string and model instances are not
     subscriptable.
     
     If anyone has any tips I am open for suggestions.
     
     thanks,
     Joshua Holt
"""

# App Engine Imports
import logging
import os
import datetime
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson
from google.appengine.api.labs import taskqueue

# Data Model Imports
import models
from models import User
#from models import Party

# Helper Imports
import helpers,notification

class UsersHandler(webapp.RequestHandler):
  
  # Retrieve a list of all the Users.
  def get(self):
    if  len(self.request.params) == 0:
      users_json = helpers.build_list_json(User.all())
      # Set the response content type and dump the json
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(users_json))
    else:
      users_json = []
      
      # Set the response content type and dump the json
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(users_json))
  
  # Create a new User
  def post(self):

    user_json = simplejson.loads(self.request.body)
    user = helpers.apply_json_to_model_instance(User(), user_json)
    user.authToken = helpers.generateAuthToken()
    user.put()
    guid = user.key().id_or_name()
    new_url = "/gamp-server/user/%s" % guid
    user_json["id"] = guid
    self.response.set_status(201, "User created")
    self.response.headers['Location'] = new_url
    self.response.headers['Content-Type'] = 'text/json'
    self.response.out.write(simplejson.dumps(user_json))


class UserHandler(webapp.RequestHandler):
  # retrieve the user with a given id
  def get(self, guid):
    # find the matching user
    key = db.Key.from_path('User', int(guid))
    user = db.get(key)
    if not user == None:
      guid = "%s" % user.key().id_or_name()
      
      user_json = { "id": "%s" % guid,
        "name": user.name,
        "loginName": user.loginName, "role": user.role,
        "preferences": user.preferences if user.preferences != None else {},
        "authToken": user.authToken if user.authToken != None else '',
        "email": user.email if user.email != '' else '',
        "createdAt": user.createdAt if user.createdAt != None else 0,
        "updatedAt": user.updatedAt if user.updatedAt != None else 0 }
      
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(user_json))
    
    else:
      self.response.set_status(404, "User not found [%s]" % guid)
  
  # Update an existing record
  def put(self, guid):
    # find the matching user
    key = db.Key.from_path('User', int(guid))
    user = db.get(key)
    if not user == None:
      
      # collect the data from the record
      user_json = simplejson.loads(self.request.body)
      # The following keeps Guests and Developers and Testers from being able
      # to change their role.
      currentUserId = self.request.params['UUID']
      cukey = db.Key.from_path('User', int(currentUserId))
      cuser = db.get(cukey)
      if str(user.role) != user_json['role'] and str(cuser.role) != "_Manager":
        user_json['role'] = str(user.role)
        self.response.set_status(401, "Not Authorized")
      # update the record
      user = helpers.apply_json_to_model_instance(user, user_json)
      # save the record
      user.put()
      # return the same record...
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(user_json))
    else:
      self.response.set_status(404, "User not found")
  
  # delete the user with a given id
  def delete(self, guid):
    self.response.set_status(401, "Not Authorized")


def main():
  application = webapp.WSGIApplication([
    (r'/gamp-server/user?$', UsersHandler),
    (r'/gamp-server/user/([^\.]+)?$', UserHandler)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()