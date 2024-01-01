#!/bin/bash

docker run \
    --name=ollama-web-ui \
    --hostname=ollama-web-ui \
    --workdir=/app/backend \
    -p 3000:8080 \
    --restart=always \
    --env=PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    --env=LANG=C.UTF-8 \
    --env=GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D \
    --env=PYTHON_VERSION=3.11.4 \
    --env=PYTHON_PIP_VERSION=23.1.2 \
    --env=PYTHON_SETUPTOOLS_VERSION=65.5.1 \
    --env=PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/0d8570dc44796f4369b652222cf176b3db6ac70e/public/get-pip.py \
    --env=PYTHON_GET_PIP_SHA256=96461deced5c2a487ddc65207ec5a9cffeca0d34e7af7ea1afc470ff0d746207 \
    --env=ENV=prod \
    --env=OLLAMA_API_BASE_URL=/ollama/api \
    --env=WEBUI_AUTH= \
    --env=WEBUI_DB_URL= \
    --env=WEBUI_JWT_SECRET_KEY=SECRET_KEY \
    --label='org.opencontainers.image.created=2023-11-25T19:33:00.421Z' \
    --label='org.opencontainers.image.description=ChatGPT-Style Web UI Client for Ollama 🦙' \
    --label='org.opencontainers.image.licenses=MIT' \
    --label='org.opencontainers.image.revision=bea9eea681df72357fc7e405173076e5388a5399' \
    --label='org.opencontainers.image.source=https://github.com/ollama-webui/ollama-webui' \
    --label='org.opencontainers.image.title=ollama-webui' \
    --label='org.opencontainers.image.url=https://github.com/ollama-webui/ollama-webui' \
    --label='org.opencontainers.image.version=main' \
    --add-host host.docker.internal:host-gateway \
    --runtime=runc -d ghcr.io/ollama-webui/ollama-webui:main