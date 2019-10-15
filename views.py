from flask import Blueprint, render_template, request, redirect, url_for
import requests
import urllib3
import xmltodict
from .models import Temperature
from . import db
main = Blueprint('main',__name__)

@main.route('/')
def index():
    temps = Temperature.query.all()
    return render_template('index.html',temps = temps)

#@main.route('/temperature')
#def temperature():
#    return render_template('temperature.html')

@main.route('/',methods=['POST'])
def temperature_post():
    city = request.form['location']
    http = urllib3.PoolManager()
    url = 'https://www.yr.no/place/Norway/Telemark/Sauherad/'+city+'/forecast.xml'
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    for i in range(len(data['weatherdata']['forecast']['tabular']['time'])):
        location = data['weatherdata']['location']['name']
        date_from = data['weatherdata']['forecast']['tabular']['time'][i]['@from']
        date_to = data['weatherdata']['forecast']['tabular']['time'][i]['@to']
        temp = data['weatherdata']['forecast']['tabular']['time'][i]['temperature']['@value']
        new_temp = Temperature(location=location,fromDate=date_from,toDate=date_to,temperature=temp)
        db.session.add(new_temp)
        db.session.commit()
    return redirect(url_for('main.index'))
