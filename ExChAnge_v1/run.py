from app import app
from app.extensions import db
import json

with open('config.json') as config_file:
    config = json.load(config_file)
    host = config['host']
    port = config['port']

if __name__ == "__main__":
    db.create_all()
    app.run(host=host,port=port,debug=True)
