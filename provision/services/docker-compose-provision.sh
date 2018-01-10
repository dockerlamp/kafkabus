#!/bin/bash

docker-compose down
docker-compose build
./up-required.sh
docker-compose logs -f |& tee logs/kafkabus-terminals.log