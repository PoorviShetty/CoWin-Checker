from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import os
from datetime import datetime
from model import LocationForm, PincodeForm

app = Flask(__name__)
now = datetime.today().strftime('%d-%m-%Y')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def get_districts(state_id):
    r = requests.get(
        'https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + str(state_id))
    districts = list()
    for district in json.loads(r.text)['districts']:
        districts.append((district["district_id"], district["district_name"]))
    return districts


@app.route('/', methods=['GET', 'POST'])
def index():
    loc_form = LocationForm()
    pin_form = PincodeForm()
    state_id = 1
    loc_form.District.choices = get_districts(state_id)

    if loc_form.validate_on_submit() and loc_form.Loc_Submit.data:
        return redirect(url_for("get_by_district", district_id=loc_form.District.data))

    if pin_form.validate_on_submit() and pin_form.Pin_Submit.data:
        return redirect(url_for("get_by_pin", pincode=pin_form.Pincode.data))

    return render_template('index.html', loc_form=loc_form, pin_form=pin_form)


@app.route('/getdistrict/<state>')
def district(state):
    districts = get_districts(state)
    return jsonify({'districts': districts})


@app.route("/pin/<pincode>", methods=["GET"])
def get_by_pin(pincode):
    params = {
        'pincode': pincode,
        'date': now
    }
    r = requests.get(
        'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin',
        params=params)
    return render_template('pin.html', data=json.loads(r.text)['centers'], pincode=pincode, type='Pincode')


@app.route("/district/<district_id>", methods=["GET"])
def get_by_district(district_id):
    params = {
        'district_id': district_id,
        'date': now
    }
    r = requests.get(
        'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict',
        params=params)
    return render_template('pin.html', data=json.loads(r.text)['centers'], district=json.loads(r.text)['centers'][0]['district_name'], type='District')


if __name__ == '__main__':
    app.run()
