from app import app
from app.extensions import db
import json
import os

with open(os.path.dirname(os.path.abspath(__file__))+'/config.json') as config_file:
    config = json.load(config_file)
    host = config['host']
    port = config['port']

if __name__ == "__main__":
    db.create_all()
    app.run(host=host,port=port,debug=True)
