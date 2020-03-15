import glob
import hashlib
import os
import random
import string
import uuid

import requests
from flask import Flask, jsonify, request, send_from_directory, Response
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024


def __get_random_dir(seed=None):
    if seed is not None:
        random.seed(seed)
    return "".join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))



@app.route("/", methods=["GET"])
def root():
    return """
<form action="/" method="post" enctype="multipart/form-data">
    <input type="file" name="file" id="file">
    <input type="submit" value="Upload" name="submit">
</form>
"""

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

@app.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify(error="File is missing!"), 400

    file = request.files["file"]
    filename = file.filename
    #seed = hashlib.sha1(file.read()).digest()
    #random_dir = __get_random_dir(seed=seed)
    #fdir = os.path.join(settings.FILES_DIR, random_dir)
    #os.makedirs(fdir, exist_ok=True)
    filepath = os.path.join('./files', filename)
    file.save(filepath)
    put_tiddler(filename, file.mimetype)

    return jsonify(filename=f'{filepath}')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
