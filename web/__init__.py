import yaml, os
from flask import Flask

# Set some globals
WEB_ROOT = os.path.join(os.getcwd(), "web")

# Get the config file
config_file = os.path.join(WEB_ROOT, "config.yaml")
config_yaml = open(config_file, "r")
config = yaml.load(config_yaml)
config_yaml.close()

app = Flask(__name__)
app.secret_key = config["server"]["secret_key"]

# Any normal web routes
import web.routes.root

# Agency related stuff
import web.routes.agency