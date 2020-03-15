import glob
import hashlib
import os
import random
import string
import uuid

import requests
from flask import Flask, jsonify, request, send_from_directory, Response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
auth = HTTPBasicAuth()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024


def __get_random_dir(seed=None):
    if seed is not None:
        random.seed(seed)
    return "".join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))



def put_tiddler(filename, mimetype):
    print('info', mimetype)
    uri = 'https://dndwiki.d1v3.de' + '/recipes/default/tiddlers/' + filename
    data = {
      "creator": "matthias",
      "text": "",
      "title": filename,
      "tags": "image [[external image]]",
      "type": mimetype,
      "fields": {
              "_canonical_uri": f"./files/{filename}",
            },
    }
    resp = requests.put(uri, json=data, auth=('matthias', 'dnd5e'), headers={'X-Requested-With': 'TiddlyWiki'})
    print(resp)
    print(resp.content)
    pass

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return jsonify(dict(
        status=status_code,
        msg=msg,
    ))

users = {
        "matthias": generate_password_hash("dnd5e"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@auth.login_required
@app.route("/")
def index():
    return render_template("index.html")

@auth.login_required
@app.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify(error="File is missing!"), 400

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        filepath = os.path.join('./files', filename)
        file.save(filepath)
        put_tiddler(filename, file.mimetype)
        if is_ajax:
            return ajax_response(True, filepath)
        else:
            return jsonify(filename=f'{filepath}')


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    names = []

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = os.path.join('files', filename)
        upload.save(destination)
        names.append(filename)
        put_tiddler(filename, upload.mimetype)

    if is_ajax:
        return ajax_response(True, names)
    else:
        return redirect(url_for("index")),



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
