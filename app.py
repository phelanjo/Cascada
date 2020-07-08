from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
  user=os.getenv("POSTGRES_USER"),
  pw=os.getenv("POSTGRES_PW"),
  url=os.getenv("POSTGRES_URL"),
  db=os.getenv("POSTGRES_DB")
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Waterfall(db.Model):
  __tablename__ = 'waterfall'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))
  height = db.Column(db.String(200))
  latitude = db.Column(db.String(200))
  longitude = db.Column(db.String(200))

  def __init__(self, name, height, latitude, longitude):
    self.name = name
    self.height = height
    self.latitude = latitude
    self.longitude = longitude

db.create_all()

@app.route('/fetch_all/', methods=['GET'])
def fetch_all():
  waterfalls = Waterfall.query.all()
  list_of_waterfalls = []

  for waterfall in waterfalls:
    list_of_waterfalls.append({
      'name': waterfall.name,
      'height': waterfall.height,
      'latitude': waterfall.latitude,
      'longitude': waterfall.longitude
    })
  return jsonify(list_of_waterfalls)

@app.route('/fetch_waterfall_by_name/', methods=['GET'])
def fetch_waterfall_id_by_name():
  name = request.args['name']
  waterfall_id = Waterfall.query.filter_by(name=name).first().id
  return jsonify(waterfall_id)
  
@app.route('/add_waterfall/', methods=['POST'])
def add_waterfall():
  response = request.get_json()
  name, height, latitude, longitude = response['name'], response['height'], response['latitude'], response['longitude']
  waterfall = Waterfall(name, height, latitude, longitude)
  db.session.add(waterfall)
  db.session.commit()
  return jsonify(response)

@app.route('/delete_waterfall/', methods=['DELETE'])
def delete_waterfall():
  response = request.get_json()
  name = response['name']
  Waterfall.query.filter_by(name=name).delete()
  db.session.commit()
  return jsonify(response)

@app.route('/edit_waterfall/', methods=['UPDATE'])
def edit_waterfall():
  response = request.get_json()
  waterfall_id, name, height, latitude, longitude = response['waterfall_id'], response['name'], response['height'], response['latitude'], response['longitude']
  waterfall = db.session.query(Waterfall).get(waterfall_id)

  waterfall.name = name
  waterfall.height = height
  waterfall.latitude = latitude
  waterfall.longitude = longitude
  
  db.session.commit()
  return jsonify(response)

@app.after_request
def add_headers(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, UPDATE, DELETE')
  return response

if __name__ == "__main__":
  app.run(host='0.0.0.0')