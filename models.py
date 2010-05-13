""" This File holds the model definitions used in this app.
  Author: Jeremy Hulick
  Date: 05-12-2010
  Last Modified: 05-012-2010
"""

from google.appengine.ext import db

""" This File holds the model definitions used in this app.
  Author: Jeremy Hulick
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Party(polymodel.PolyModel):
  """ This is the Party Model"""
  parent_id = db.IntegerProperty(required=False)
  clinician_type_id = db.IntegerProperty(required=False)
  person_title_id = db.IntegerProperty(required=False)
  ethnicity_id = db.IntegerProperty(required=False)
  gender_id = db.IntegerProperty(required=False)
  careUnit_type_id = db.IntegerProperty(required=False)
  blood_type_id = db.IntegerProperty(required=False)
  education_level_id = db.IntegerProperty(required=False)
  religion_id = db.IntegerProperty(required=False)
  living_arrangement_id = db.IntegerProperty(required=False)
  primary_care_physician_id = db.IntegerProperty(required=False)
  type = db.StringProperty(required=False, indexed=True)
  first_name = db.StringProperty(required=False, indexed=True)
  middle_name = db.StringProperty(required=False)
  last_name = db.StringProperty(required=False, indexed=True)
  name_suffix = db.StringProperty(required=False)
  degree_name = db.StringProperty(required=False)
  maiden_name = db.StringProperty(required=False)
  known_as_name = db.StringProperty(required=False)
  last_name_soundex = db.StringProperty(required=False, indexed=True)
  last_name_metaphone = db.StringProperty(required=False, indexed=True)
  initials = db.StringProperty(required=False)
  name = db.StringProperty(required=False, indexed=True)
  birth_place = db.StringProperty(required=False)
  temp_patient_flag = db.BooleanProperty(required=True, default=False)
  birth_date = db.IntegerProperty(required=False)
  death_date = db.IntegerProperty(required=False)
  birth_date_approx = db.StringProperty(required=False)
  death_date_approx = db.StringProperty(required=False)
  position = db.IntegerProperty(required=False)
  start_date = db.IntegerProperty(required=False)
  end_date = db.IntegerProperty(required=False)
  start_date_approx = db.StringProperty(required=False)
  end_date_approx = db.StringProperty(required=False)
  record_status_id = db.IntegerProperty(required=True)
  face_sheet_update_stamp = db.IntegerProperty(required=True)

class User(Party):
  """ This is the Party Model"""
  login = db.StringProperty(required=False, indexed=True)
  salt = db.StringProperty(required=False)
  application_path = db.StringProperty(required=False)
  default_page_after_login = db.StringProperty(required=False)
  remember_token = db.StringProperty(required=False)
  crypted_password = db.StringProperty(required=False)
  crypted_pin = db.StringProperty(required=False)
  time_zone = db.StringProperty(required=False)
  password_expiration_date_time_utc = db.IntegerProperty(required=False)
  expiration_date_time_utc = db.IntegerProperty(required=False)
  locked_until_date_time_utc = db.IntegerProperty(required=False)
  last_login_date_time_utc = db.IntegerProperty(required=False)
  remember_token_expires_at = db.IntegerProperty(required=False)
  account_never_expires_flag = db.BooleanProperty(required=True, default=False)
  indefinitely_locked_flag = db.BooleanProperty(required=True, default=False)
  system_flag = db.BooleanProperty(required=True, default=False, indexed=True)
  administrator_flag = db.BooleanProperty(required=True, default=False)
  phr = db.BooleanProperty(required=True, default=False, indexed=True)
  person_id = db.StringProperty(required=False) # references party
  default_filing_center_group_id = db.IntegerProperty(required=False)  # references storage_unit