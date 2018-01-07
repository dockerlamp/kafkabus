#!/bin/bash

echo 'restarting python producer&consumer containers...'
docker-compose restart py_producer
docker-compose restart py_consumer