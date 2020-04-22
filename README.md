# A simple uploader for Tiddlwiki

This offers a simple way to upload files to a Tiddlywiki. They are stored in the files folder, which is served by the tiddlywiki node.js based server.
It adds tiddlers with references to the external file.

## Why?

I use tiddlywiki on my server. I use it also for preparing Dungeon and Dragon campaigns and add images, PDFs and so on. I noticed, that opening the wiki on a new device will download tons of MB which I do not want to access or use at that point in time at all. With external files, this does not happen.

## How

This is an example a possible docker compose file:
```
version: '2'

services:
  tiddlywiki:
    image: tiddlywiki-image
    restart: always
    ports:
      - "12345:8080"
    environment:
      - TW_WIKINAME=mywiki
      - TW_HTTPAUTH=true
      - TW_PORT=8080
      - TW_RENDERTYPE=text/plain
      - TW_LAZY=false
      - TW_SERVETYPE=text/html
      - TW_HOST=0.0.0.0
      - TW_PATHPREFIX=
    volumes:
      - '/var/docker/tiddlywiki:/var/lib/tiddlywiki'

  imgupload:
    ports:
        - "12346:5000"
    restart: always
    environment:
      - TW_UPLOAD_PATH=/upload
      - TW_URL=mywikiurl
    image: tiddlywiki-upload
    volumes:
      - "/var/docker/tiddlywiki/mywiki/files:/app/files"
```

I use it with nginx, so I configured the following reverse proxies in nginx

```
location ^~ /upload {
  proxy_pass http://127.0.0.1:12346;
  proxy_set_header X-Forwarded-For $remote_addr;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header Host $host;
  proxy_pass_header Authorization;
  proxy_redirect off;
  proxy_buffering off;
  chunked_transfer_encoding off;
  client_max_body_size 0;
  auth_basic "Members Only";
  auth_basic_user_file /var/www/.htpasswd;
  proxy_connect_timeout       300;
  proxy_send_timeout          300;
  proxy_read_timeout          300;
  send_timeout                300;
}

location ^~ / {
  proxy_pass http://127.0.0.1:12345;
  proxy_set_header X-Forwarded-User $remote_user;
  proxy_set_header X-Forwarded-For $remote_addr;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header Host $host;
  proxy_redirect off;
  proxy_buffering off;
  chunked_transfer_encoding off;
  auth_basic "Members Only";
  auth_basic_user_file /var/www/.htpasswd;
  client_max_body_size 0;
}
```

Adding the tiddler `UploadSidebar` and you get a tab, using an iFrame which offers you to upload files.

## What is wrong with it

Well, to be honest, it is nothing of style, I would like to have a better integration into tiddlywiki, but not a good idea yet.
