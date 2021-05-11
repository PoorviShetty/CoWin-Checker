from wtforms import SubmitField, SelectField, StringField, validators
from flask_wtf import FlaskForm
import requests
import json


def fetch_states():
    r = requests.get(
        'https://cdn-api.co-vin.in/api/v2/admin/location/states')
    states = list()
    for state in json.loads(r.text)['states']:
        states.append((state['state_id'], state['state_name']))
    return states


class LocationForm(FlaskForm):
    State = SelectField('State', choices=fetch_states(), validate_choice=False)
    District = SelectField('District', choices=[], validate_choice=False)
    Loc_Submit = SubmitField('Submit')


class PincodeForm(FlaskForm):
    Pincode = StringField('Pincode', [validators.DataRequired(), validators.Length(min=6, max=6)])
    Pin_Submit = SubmitField('Submit')
