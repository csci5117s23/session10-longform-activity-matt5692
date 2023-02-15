from flask import *
from authlib.integrations.flask_client import OAuth
from blueprints.login_blueprints import login_pages
import os 
import json

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.register_blueprint(login_pages)

oauth = OAuth(app)
app.oauth = oauth 

oauth.register(
    "auth0",
    client_id=os.environ["AUTH0_CLIENT_ID"],
    client_secret=os.environ["AUTH0_CLIENT_SECRET"],
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
)

@app.route("/")
def index():
    return render_template('index.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))