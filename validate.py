
from cerberus import Validator

import datetime

#program to validate a user data in a dict
userschema = {'fname': {'type':'string', 'maxlength': 45, 'regex':'^[A-z]+$', 'required':True},
        'lname': {'type':'string', 'maxlength': 45, 'regex':'^[A-z]+$', 'required': True},
        'username':{'type':'string', 'maxlength': 45, 'regex':'^[A-z0-9]+$', 'required': True},
        'password':{'type':'string', 'maxlength': 45, 'minlength':8, 'regex':'\\w+', 'required': True},
        'currentweight':{'type':'integer','min':70, 'max':600, 'required': True},
        'goalweight':{'type':'integer','min':70, 'max':600, 'required': True},
        'age':{'type':'integer','min':18, 'max':100, 'required': True},
        'height' :{'type':'integer', 'required': True},
        'startweight':{'type':'integer','min':70, 'max':600, 'required': True},
        'metrics': {'type':'integer','min':0, 'max':1, 'required': True},
        'gender': {'type':'integer','min':0, 'max':1, 'required': True},
        'watergoal': {'type':'integer','min':0, 'max':900, 'required': True}}

loginschema = {
    'username':{'type':'string', 'maxlength': 45, 'regex':'^[A-z0-9]+$', 'required': True},
    'password':{'type':'string', 'maxlength': 45, 'minlength':8, 'regex':'\\w+', 'required': True}
}

waterschema = {'amount' :  {'type':'integer','min':1.9, 'max':900,'required':True},
      'goal': {'type':'integer','min':64, 'max':900, 'required':True},
      'date': {'type':'date', 'required':True},
      'metrics':{'type':'integer','min':0, 'max':1, 'required': True}}

exerciseschema = {'calories': {'type':'integer','min':0, 'max':1000,'required':True},
      'start': {'type':'date', 'required': True},
      'end': {'type':'date', 'required': True},
      'date': {'type':'date', 'required':True},
      'name':{'type':'string', 'maxlength': 45, 'regex':'^[A-z]+$', 'required':True}}

schema2 = {'fname': {'type':'string', 'maxlength': 45, 'regex': '^[A-z]+$', 'required':True}}

schema3 = {'date': {'type':'date'}}

schema = {'name': {'type': 'string', 'regex':'^[A-z]+$', 'required': True}}
document = {'fname': 'john1'}

v = Validator(schema)
d =  datetime.date(2020, 1, 29)
n = "Mags"
dr = ''
user = {'name': ''}

water = {'amount': 123, 'goal':16, 'date':d, 'metrics':0}

what = {'date': d}



if (v.validate(user)):
    print('data is valid')
else:
    print(v.errors)
