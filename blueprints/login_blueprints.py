import os
from urllib.parse import urlencode, quote_plus

from flask import Blueprint, current_app
from flask import session, redirect, url_for

login_pages = Blueprint('login_pages', __name__, template_folder='templates')

@login_pages.route("/callback", methods=["GET", "POST"])
def callback():
    token = current_app.oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@login_pages.route("/login")
def login():
    return current_app.oauth.auth0.authorize_redirect(
        redirect_uri=url_for("login_pages.callback", _external=True)
    )


@login_pages.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": os.environ["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )
