#!/bin/bash

mkdir -p ollama.hidden

if docker ps --filter "ollama" -q >/dev/null 2>&1; then
    echo "Container is running!"
else
    docker run \
        --rm \
        --name ollama \
        -d \
        --gpus=all \
        -v ollama.hidden:/root/.ollama \
        -p 15434:15434 \
        ollama/ollama
fi
