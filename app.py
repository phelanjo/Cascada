from flask import Flask
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

print(DB_URL)

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

db.create_all()

# @app.route('/')

# @app.route('/add')

# @app.route('/edit')

if __name__ == "__main__":
  app.run()