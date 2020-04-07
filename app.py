import glob
import hashlib
import os
import random
import string
import uuid

import requests
from flask import Flask, jsonify, request, send_from_directory, Response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
app.config["APPLICATION_ROOT"] = os.getenv('TW_UPLOAD_PATH', '')

from werkzeug.wsgi import DispatcherMiddleware

def no_app(environ, start_response):
    return NotFound()(environ, start_response)

app.wsgi_app = DispatcherMiddleware(no_app, {os.getenv('TW_UPLOAD_PATH', ''): app.wsgi_app})

def put_tiddler(filename, mimetype, username):
    uri = 'https://' + os.getenv('TW_URL', 'dndwiki.d1v3.de') + '/recipes/default/tiddlers/' + filename
    if 'image' in mimetype:
        tags = "image [[external image]]"
    else:
        tags = "file [[external file]]"
    data = {
      "creator": username,
      "text": "",
      "title": filename,
      "tags": tags,
      "type": mimetype,
      "fields": {
              "_canonical_uri": f"./files/{filename}",
            },
    }
    resp = requests.put(uri, json=data, headers={'X-Requested-With': 'TiddlyWiki'})
    pass

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return jsonify(dict(
        status=status_code,
        msg=msg,
    ))

@app.route(f"/")
def index():
    return render_template("index.html")

@app.route(f"/", methods=["POST"])
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
        put_tiddler(filename, upload.mimetype, request.headers.get('x-forward-user', 'none'))

    if is_ajax:
        return ajax_response(True, names)
    else:
        return redirect(url_for("index")),



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
