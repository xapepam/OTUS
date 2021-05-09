import os
import json
 
from flask import Flask
from flask import request

app = Flask(__name__)
 
config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ.get('HOSTNAME'),
    'GREETING': os.environ.get('GREETING', 'Hello'),
}
 
@app.route("/")
def hello():
    return config['GREETING'] + ' from ' + config['HOSTNAME'] + '!'
 
@app.route("/config")
def configuration():
    return json.dumps(config)
 
@app.route('/list')
def list():
    from sqlalchemy import create_engine
 
    engine = create_engine(config['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = connection.execute("select id, name from clients;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

@app.route('/create', methods=['GET', 'POST'])
def create(**kwargs):
    from sqlalchemy import create_engine
    clientname = request.args.get('clientname')
    engine = create_engine(config['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = [connection.execute("insert into clients (name) values ('{}')".format(key)) for key in kwargs.items()]
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
